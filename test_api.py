# Testing my API

from main import server

from flask import json







def test_post_request():
    """This function is used to test the API I built in the main.py file.
    It sends a json object and I should get """
    response = server.test_client().post(
        '/sentiment-analysis-long',
        data=json.dumps({'title': 'canto1', 'input_text': "Midway on our life's journey, I found myself In dark woods the right road lost. To tell About "
                                                          "those woods is hard--so tangled and rough And savage that thinking of it now, I feel The old fear stirring: "
                                                          "death is hardly more bitter. And yet, to treat the good I found there as well I'll tell what I saw, though how I came to enter I cannot well say, being so full of sleep Whatever moment it was I began to blunder Off the true path. But when I came to stop Below a hill that marked one end of the valley That had pierced my heart with terror, "
                                                          "I looked up Toward the crest and saw its shoulders already Mantled in rays of that bright planet that shows The road to everyone, whatever our journey."
                         }),
        content_type='application/json',
    )

    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data['neg'] == 1

{'title': 'The Terminator 2', 'input_text': "In 1995, John Connor is living in Los Angeles with his foster parents. His mother, Sarah Connor, had been preparing him throughout his childhood for his future role as the human resistance leader against Skynet, the artificial intelligence that will be given control of the United States' nuclear missiles and initiate a nuclear holocaust on August 29, 1997, known thereafter as 'Judgment Day'. However, Sarah was arrested and imprisoned at a mental hospital after attempting to bomb a computer factory. In 2029, Skynet sends a new Terminator, designated as T-1000, back in time to kill John. The T-1000 is an advanced prototype made out of liquid metal (referred to as 'mimetic polyalloy') that gives it the ability to take on the shape and appearance of almost anything it touches, and to transform its arms into blades and other shapes at will. The T-1000 arrives, kills a police officer, and assumes his identity; he also uses the police computer to track down John. Meanwhile, the future John Connor has sent back a reprogrammed Model 101 Terminator to protect his younger self. The Terminator and the T-1000 converge on John in a shopping mall, and a chase ensues after which John and the Terminator escape together on a motorcycle. Fearing that the T-1000 will kill Sarah in order to get to him, John orders the Terminator to help free her, after discovering that the Terminator must follow his orders. They encounter Sarah as she is escaping from the hospital, although she is initially reluctant to trust the Model 101. After the trio escape from the T-1000 in a police car, the Terminator informs John and Sarah about Skynet's history.[a] Sarah learns that the man most directly responsible for Skynet's creation is Miles Bennett Dyson, a Cyberdyne Systems engineer working on a revolutionary new microprocessor that will form the basis for Skynet. Sarah gathers weapons from an old friend and plans to flee with John to Mexico, but after having a nightmare about Judgment Day, she instead sets out to kill Dyson in order to prevent Judgment Day from occurring. Finding him at his home, she wounds him but finds herself unable to kill him in front of his family. John and the Terminator arrive and inform Dyson of the future consequences of his work. They learn that much of his research has been reverse engineered from the damaged CPU and the right arm of the previous Terminator who attacked Sarah back in 1984. Convincing him that these items and his designs must be destroyed, they break into the Cyberdyne building, retrieve the CPU and the arm, and set explosives to destroy Dyson's lab. The police arrive and Dyson is fatally shot, but he rigs an improvised dead man's switch that detonates the explosives when he dies. The T-1000 pursues the surviving trio, eventually cornering them in a steel mill. The T-1000 and Model 101 fight and the more advanced model seriously damages and shuts down the Model 101. However, unbeknownst to the T-1000, the Model 101 brings itself back online using an alternate power source. The T-1000 was about to kill John and Sarah, but the Model 101 blasts it into a crucible of molten steel with a grenade launcher, dissolving and destroying it. John tosses the arm and CPU of the original Terminator into the vat as well. As Sarah expresses relief that the ordeal is over, the Terminator explains that to ensure that his CPU is not reverse engineered it must also be destroyed. It asks Sarah to assist in lowering it into the vat of molten steel, since it is unable to 'self-terminate'. Although John begs and eventually orders the Terminator to reconsider, it makes the decision to defy him, bids them farewell and hugs a tearful John before it is lowered into the vat, giving a final thumbs-up as it disappears within. John and Sarah drive down a highway with the latter having a renewed hope for the future based on the Terminator's actions."}