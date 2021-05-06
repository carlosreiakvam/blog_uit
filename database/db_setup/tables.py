from extensions import db
from mysql.connector import errorcode, Error
from flask import current_app

TABLES = {}

TABLES["bruker"] = """
CREATE TABLE `bruker` (
  `bruker_navn` VARCHAR(24) NOT NULL,
  `bruker_epost` VARCHAR(45) NOT NULL,
  `bruker_passord_hash` VARCHAR(100) NOT NULL,
  `bruker_opprettet` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `bruker_fornavn` VARCHAR(45) NOT NULL,
  `bruker_etternavn` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`bruker_navn`),
  UNIQUE INDEX `bruker_navn_UNIQUE` (`bruker_navn` ASC))
ENGINE = InnoDB
"""

TABLES["blog"] = """
CREATE TABLE `blog` (
  `blog_prefix` VARCHAR(20) NOT NULL,
  `blog_navn` VARCHAR(45) NOT NULL,
  `bruker_navn` VARCHAR(24) NOT NULL,
  `blog_opprettet` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`blog_prefix`, `bruker_navn`),
  UNIQUE INDEX `blog_prefix_UNIQUE` (`blog_prefix` ASC),
  CONSTRAINT `fk_blog_brukere`
    FOREIGN KEY (`bruker_navn`)
    REFERENCES `bruker` (`bruker_navn`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
"""

TABLES["innlegg"] = """
CREATE TABLE `innlegg` (
  `innlegg_id` INT NOT NULL AUTO_INCREMENT,
  `innlegg_tittel` VARCHAR(100) NOT NULL,
  `innlegg_innhold` TEXT NOT NULL,
  `innlegg_dato` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `innlegg_endret` DATETIME NULL,
  `innlegg_treff` INT NULL DEFAULT 0,
  `blog_prefix` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`innlegg_id`),
  UNIQUE INDEX `innlegg_id_UNIQUE` (`innlegg_id` ASC),
  INDEX `fk_innlegg_blog1_idx` (`blog_prefix` ASC),
  FULLTEXT INDEX `idx_innlegg_tittel_FULLTEXT` (`innlegg_tittel`),
  FULLTEXT INDEX `idx_innlegg_innhold_FULLTEXT` (`innlegg_innhold`),
  CONSTRAINT `fk_innlegg_blog1`
    FOREIGN KEY (`blog_prefix`)
    REFERENCES `blog` (`blog_prefix`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
"""

TABLES["kommentar"] = """
CREATE TABLE `kommentar` (
  `kommentar_id` INT NOT NULL AUTO_INCREMENT,
  `kommentar_innhold` TINYTEXT NULL,
  `kommentar_dato` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `bruker_navn` VARCHAR(24) NOT NULL,
  `innlegg_id` INT NOT NULL,
  PRIMARY KEY (`kommentar_id`, `bruker_navn`, `innlegg_id`),
  INDEX `fk_kommentar_brukere1_idx` (`bruker_navn` ASC),
  INDEX `fk_kommentar_innlegg1_idx` (`innlegg_id` ASC),
  UNIQUE INDEX `kommentar_id_UNIQUE` (`kommentar_id` ASC),
  CONSTRAINT `fk_kommentar_brukere1`
    FOREIGN KEY (`bruker_navn`)
    REFERENCES `brukere` (`bruker_navn`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_kommentar_innlegg1`
    FOREIGN KEY (`innlegg_id`)
    REFERENCES `innlegg` (`innlegg_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
"""

TABLES["tag"] = """
CREATE TABLE `tag` (
  `tag_navn` VARCHAR(45) NOT NULL,
  `innlegg_id` INT NOT NULL,
  PRIMARY KEY (`innlegg_id`, `tag_navn`),
  INDEX `fk_tag_innlegg1_idx` (`innlegg_id` ASC),
  CONSTRAINT `fk_tag_innlegg1`
    FOREIGN KEY (`innlegg_id`)
    REFERENCES `innlegg` (`innlegg_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
"""

TABLES["kommentar_logg"] = """
CREATE TABLE `kommentar_logg` (
  `kommentar_id` INT NOT NULL,
  `kommentar_innhold` TINYTEXT NULL,
  `kommentar_dato` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `bruker_navn` VARCHAR(24) NOT NULL,
  `innlegg_id` INT NOT NULL,
  `slettet_dato` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`kommentar_id`, `bruker_navn`, `innlegg_id`),
  INDEX `fk_kommentarer_brukere1_idx` (`bruker_navn` ASC),
  INDEX `fk_kommentarer_innlegg1_idx` (`innlegg_id` ASC),
  CONSTRAINT `fk_kommentarer_brukere10`
    FOREIGN KEY (`bruker_navn`)
    REFERENCES `brukere` (`bruker_navn`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_kommentarer_innlegg10`
    FOREIGN KEY (`innlegg_id`)
    REFERENCES `innlegg` (`innlegg_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
"""

TABLES["vedlegg"] = """
CREATE TABLE `vedlegg` (
  `vedlegg_id` VARCHAR(32),
  `vedlegg_navn` VARCHAR(45) NOT NULL,
  `bruker_navn` VARCHAR(24) NOT NULL,
  PRIMARY KEY (`vedlegg_id`, `bruker_navn`),
  UNIQUE INDEX `vedlegg_id_UNIQUE` (`vedlegg_id` ASC),
  CONSTRAINT `fk_vedlegg_brukere1`
    FOREIGN KEY (`bruker_navn`)
    REFERENCES `brukere` (`bruker_navn`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
"""


def create_tables():
    cursor = db.connection.cursor()
    cursor.execute("USE {}".format(current_app.config['DATABASE_NAME']))
    for table_name, table_definition in TABLES.items():
        try:
            print(f"Creating table {table_name}: ", end='')
            cursor.execute(table_definition)
        except Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    cursor.close()


def drop_tables():
    cursor = db.connection.cursor()
    cursor.execute("USE {}".format(current_app.config['DATABASE_NAME']))
    tables = ["vedlegg", "kommentar_logg", "tag", "kommentar", "innlegg", "blog", "bruker"]
    for table_name in tables:
        try:
            print(f"Dropping table {table_name}: ", end="")
            cursor.execute("drop table {}".format(table_name))
        except Error as err:
            if err.errno == errorcode.ER_BAD_TABLE_ERROR:
                print("Does not exist")
            else:
                print(err.msg)
        else:
            print("OK")

    cursor.close()
