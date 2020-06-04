import sys
import os
from cmd_parser import CmdParser
from data_generator import DataGenerator
from data_processor import DataProcessor
from data_visualizer import DataVisualizer

cmd_parser = CmdParser()
cmd_parser.parse(sys.argv[1:])
print("Using input: state={}, keywords={}".format(cmd_parser.state, cmd_parser.keywords))

data_generator = DataGenerator(cmd_parser.state, cmd_parser.keywords)
print("\n=========Generating data========")
data_generator.run()
print(data_generator.covid_data.head(5))
print(data_generator.trend_data.head(5))
data_frames = [data_generator.covid_data, data_generator.trend_data]

print("\n=========Processing data========")
data_processor = DataProcessor(data_generator.keywords, data_frames)
data_processor.run()
print("\nProcessed COVID Data columns\n", data_processor.clean_data_frame[0].columns)
print("\nProcessed GoogleTrends Data columns\n", data_processor.clean_data_frame[1].columns)
agg_data_frame = data_processor.agg_data_frame
curr_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
output_dir = curr_dir + "/outputs/"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
csv_file_path = output_dir + data_generator.state + "_agg_data_frame.csv"
agg_data_frame.to_csv(csv_file_path)
print("\nAggregated cleaned dataframe saved at {}\n".format(csv_file_path))

print("\n=========Visualizing data========")
data_visualizer = DataVisualizer(data_generator.state, data_generator.keywords, data_processor.agg_data_frame)
data_visualizer.show()
img_file_path = output_dir + data_generator.state + "_coronavirus_trend_impacts.png"
print("\nVisualization saved at {}\n".format(img_file_path))