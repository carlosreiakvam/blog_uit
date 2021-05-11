from models.vedlegg import Vedlegg


def opprett_vedlegg():
    vedlegg = [
        {
            "bruker_navn": "tyt005",
            "vedlegg_navn": "duckface.jpg",
            "vedlegg_id": "e59aaab51e73433dba83ab3f1b00b831",
            "vedlegg_mimetype": "image/jpeg"
        },
        {
            "bruker_navn": "jbi017",
            "vedlegg_navn": "UiT_Logo_Eng_2l_Bla_RGB.png",
            "vedlegg_id": "c7719253eb944556a4954c7d9c83f512",
            "vedlegg_mimetype": "image/png"
        }
    ]
    print(20 * "-")
    for _vedlegg in vedlegg:
        vedlegg_object = Vedlegg(**_vedlegg)
        vedlegg_object = vedlegg_object.insert()
        print(f"Opprettet vedlegg: {vedlegg_object.vedlegg_id}")
