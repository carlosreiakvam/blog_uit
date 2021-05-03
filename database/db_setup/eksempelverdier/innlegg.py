import random

from flask import current_app

from models.innlegg import Innlegg

BLOGGER = ["tyt005", "jbi017", "hro047", "cre032"]
TAGGER = ["Rosa", "Matlaging", "Kaker", "Duckface", "Sol", "Varme", "Eksamen", "Narvik", "UiT", "Programmering",
          "Python", "Flask"]

KOMMENTARER = [
    "Kjempefin blog!",
    "Kan vi få mer rosa?",
    "Gleder meg til neste innlegg!"
]


def opprett_innlegg():
    innlegg = [
        {
            "innlegg_tittel": "Innlegg med lang tekst",
            "innlegg_innhold": """
        <p>As hermit crabs grow, they require larger shells. Since suitable intact gastropod shells are sometimes a limited resource, vigorous competition often occurs among hermit crabs for shells. The availability of empty shells at any given place depends on the relative abundance of gastropods and hermit crabs, matched for size. An equally important issue is the population of organisms that prey upon gastropods and leave the shells intact.[8] Hermit crabs kept together may fight or kill a competitor to gain access to the shell they favour. However, if the crabs vary significantly in size, the occurrence of fights over empty shells will decrease or remain nonexistent.[9] Hermit crabs with too-small shells cannot grow as fast as those with well-fitting shells, and are more likely to be eaten if they cannot retract completely into the shell.[10] Several Hermit crabs on the beach at Amami Ōshima in Japan.</p>

        <p>As the hermit crab grows in size, it must find a larger shell and abandon the previous one. Several hermit crab species, both terrestrial and marine, have been observed forming a vacancy chain to exchange shells.[9] When an individual crab finds a new empty shell it will leave its own shell and inspect the vacant shell for size. If the shell is found to be too large, the crab goes back to its own shell and then waits by the vacant shell for up to 8 hours. As new crabs arrive they also inspect the shell and, if it is too big, wait with the others, forming a group of up to 20 individuals, holding onto each other in a line from the largest to the smallest crab. As soon as a crab arrives that is the right size for the vacant shell and claims it, leaving its old shell vacant, then all the crabs in the queue swiftly exchange shells in sequence, each one moving up to the next size.[11] Hermit crabs often &quot;gang up&quot; on one of their species with what they perceive to be a better shell, and pry its shell away from it before competing for it until one takes it over.[12]</p>
        
        <p>There are cases when seashells are not available and hermit crabs will use alternatives such as tin cans, custom-made shells, or any other types of debris, which often proves fatal to the hermit crabs (as they can climb into, but not out of, slippery plastic debris).[13] This can even create a chain reaction of fatality, because a dead hermit crab will release a signal to tell others that a shell is available, luring more hermit crabs to their deaths.</p>
        
        <p>For some larger marine species, supporting one or more sea anemones on the shell can scare away predators. The sea anemone benefits, because it is in position to consume fragments of the hermit crab&#39;s meals. Other very close symbiotic relationships are known from encrusting bryozoans and hermit crabs forming bryoliths.[14]</p>
        
        <p>&nbsp;</p>
        
        <pre>
        <code class="language-python">from flask import Flask
        
        from blueprints.auth import router as auth_blueprint
        from blueprints.blog import router as blog_blueprint
        from blueprints.hovedside import router as hovedside_blueprint
        from blueprints.vedlegg import router as vedlegg_blueprint
        from config import config
        from errors import page_not_found
        from extensions import ck, csrf, db, login_manager
        from models.bruker import Bruker
        
        
        def create_app(config_name="default"):
            app = Flask(__name__)
            app.config.from_object(config[config_name])
        
            db.init_app(app)
            login_manager.init_app(app)
            ck.init_app(app)
            csrf.init_app(app)
        
            @login_manager.user_loader
            def load_user(user_id):
                return Bruker.get_user(user_id)
        
            app.register_blueprint(auth_blueprint)
            app.register_blueprint(hovedside_blueprint)
            app.register_blueprint(blog_blueprint)
            app.register_blueprint(vedlegg_blueprint)
            app.register_error_handler(404, page_not_found)
        
            return app
        
        
        if __name__ == '__main__':
            flask_app = create_app(config_name="development")
            flask_app.run()</code></pre>
        
        <p>&nbsp;</p>
        
        <p>Tekst hentet fra wikipedia</p>
        
        <p>&nbsp;</p>

        """
        },
        {
            "innlegg_tittel": "Heia bloggen!",
            "innlegg_innhold": """
            <h1>DTE-2509</h1>

            <p><img alt="" src="{}/vedlegg/c7719253eb944556a4954c7d9c83f512" style="height:73px; width:400px" /></p>
            
            <p>&nbsp;</p>
            
            <p>Datateknikk ved UiT er topp!</p>
            
            <p>&nbsp;</p>
            """.format(current_app.config['URL_PREFIX'])
        },
        {
            "innlegg_tittel": "Heia igjen Bloggen!",
            "innlegg_innhold": """
            <p><img alt="hei hei" src="{}/vedlegg/e59aaab51e73433dba83ab3f1b00b831" style="height:390px; width:694px" /></p>

            <p>Heia bloggen, se s&aring; fine bilder jeg fant p&aring; nettet</p>
            
            <p>&nbsp;</p>
            
            <p><strong>BOOOOOLD</strong></p>
            
            <p>&nbsp;</p>
            
            <p><code>monospace font ogs&aring;</code></p>
            
            <p>&nbsp;</p>
            """.format(current_app.config['URL_PREFIX'])
        },
        {
            "innlegg_tittel": "Hvor mye rosa er for mye rosa?",
            "innlegg_innhold": "hei hei"
        }
    ]
    print(20 * "-")
    for blog in BLOGGER:
        for _innlegg in innlegg:
            innlegg_object = Innlegg(blog_prefix=blog, **_innlegg)
            innlegg_object = innlegg_object.insert()
            tagger = random.sample(TAGGER, 3)
            for tag in tagger:
                innlegg_object.add_tag(tag)
            for bruker, kommentar in zip([x for x in BLOGGER if x != blog], KOMMENTARER):
                innlegg_object.add_kommentar(kommentar_innhold=kommentar, bruker_navn=bruker)
            slett = innlegg_object.add_kommentar(kommentar_innhold="Den her vil jeg slette!", bruker_navn=blog)
            slett.delete_kommentar()
            print(f"Opprettet innlegg: {blog}: {innlegg_object.innlegg_tittel}")
