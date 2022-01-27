import json
import unittest

from google.protobuf.json_format import MessageToDict

from data import load
from parser import parse


class TestParser(unittest.TestCase):
    def test_jan_2020(self):
        self.maxDiff = None
        # Json com a saida esperada
        with open('src/output_test/expected/expected_02_2018.json', 'r') as fp:
            expected = json.load(fp)
   
        files = ['src/output_test/sheets/membros-ativos-contracheque-02-2018.xlsx',
                 'src/output_test/sheets/membros-ativos-verbas-indenizatorias-02-2018.xlsx']
                 
        dados = load(files, '2018', '02', 'src/output_test')
        result_data = parse(dados, 'mpsc/02/2018', '02', '2018')
        # Converto o resultado do parser, em dict
        result_to_dict = MessageToDict(result_data)

        self.assertEqual(expected, result_to_dict)


if __name__ == '__main__':
    unittest.main()
    