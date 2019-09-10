from keras.models import load_model
from keras import backend as K
import tensorflow as tf
import argparse

K.set_learning_phase(0)

def freeze_session(session, keep_var_names=None, output_names=None, clear_devices=True):
    """
    Freezes the state of a session into a pruned computation graph.

    @param session The TensorFlow session to be frozen.
    @param keep_var_names A list of variable names that should not be frozen,
                          or None to freeze all the variables in the graph.
    @param output_names Names of the relevant graph outputs.
    @param clear_devices Remove the device directives from the graph for better portability.
    @return The frozen graph definition.
    """
    from tensorflow.python.framework.graph_util import convert_variables_to_constants
    graph = session.graph
    with graph.as_default():
        freeze_var_names = list(set(v.op.name for v in tf.global_variables()).difference(keep_var_names or []))
        output_names = output_names or []
        output_names += [v.op.name for v in tf.global_variables()]
        # Graph -> GraphDef ProtoBuf
        input_graph_def = graph.as_graph_def()
        if clear_devices:
            for node in input_graph_def.node:
                node.device = ""
        frozen_graph = convert_variables_to_constants(session, input_graph_def,
                                                      output_names, freeze_var_names)
        return frozen_graph



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
      '--input_dir',
      type=str,
      default='../models/trained_keras_models/simple_CNN.530-0.65.hdf5',
      help='Path to trained keras model.'
    )
    parser.add_argument(
      '--output_dir',
      type=str,
      default='../models/converted_tensorflow_models',
      help='Path for converted tensorflow model.'
    )
    parser.add_argument(
        '--graph_name',
        type=str,
        default='tf_model.pb',
        help='Name of the tensorflow graph with .pb extension'
    )


    args = parser.parse_args()
    model = load_model(args.input_dir)

    frozen_graph = freeze_session(K.get_session(),
                              output_names=[out.op.name for out in model.outputs])

    tf.train.write_graph(frozen_graph, args.output_dir,args.graph_name, as_text=False)

    print('model input name: ', model.inputs)
    print('model output name: ', model.outputs)
