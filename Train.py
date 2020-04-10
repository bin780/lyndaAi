import io
import json
def init(seed):
    with io.open("Dataset/dataset.json",encoding="utf8") as f:
        sample_dataset = json.load(f)

    print("initialising  Lynda")

    from snips_nlu import SnipsNLUEngine

    from snips_nlu.default_configs import CONFIG_EN

    nlu_engine = SnipsNLUEngine(config=CONFIG_EN, random_state=seed)


    nlu_engine.fit(sample_dataset)

    print("momdel created")





    nlu_engine.persist('model')

    print("model dumped")



def load_model():
    from snips_nlu import SnipsNLUEngine as se
    model=se.from_path('model')
    return model





if __name__ == '__main__':
    init(42)




