import json
from unittest import TestCase
from re import match

from sqlalchemy import Column, String, Integer
import app.utils as utils
from app.app import create_app
from app.logging import pcf_logger, formatter
import app.database as db

class TestModel(db.Base):

    __tablename__ = 'test_model'

    str_field = Column(String(10), primary_key=True)
    int_field = Column(Integer())

class TestSerializer(TestCase):

    @classmethod
    def setUpClass(cls):
        create_app()
        TestModel.__table__.create(db.engine)
        cls.dict1 = {'int_field': 1, 'str_field': 'test1'}
        cls.str1 = '{"int_field": 1, "str_field": "test1"}'
        cls.dict2 = {'int_field': 2, 'str_field': 'test2'}
        cls.str2 = '{"int_field": 2, "str_field": "test2"}'

    @classmethod
    def test_model_load(cls):
        ''' Should serialize dict into object '''
        test_model = TestModel.load(cls.dict1)
        assert test_model.str_field == 'test1'
        assert test_model.int_field == 1

    @classmethod
    def test_model_loads(cls):
        ''' Should serialize json str into object '''
        test_model = TestModel.loads(cls.str1)
        assert test_model.str_field == 'test1'
        assert test_model.int_field == 1

    @classmethod
    def test_model_dump(cls):
        ''' Should deserialize obj into dict '''
        test_model = TestModel.load(cls.dict1)
        assert test_model.dump() == cls.dict1

    @classmethod
    def test_model_dumps(cls):
        ''' Should deserialize obj into json str '''
        test_model = TestModel.loads(cls.str1)
        data = json.loads(test_model.dumps())
        assert data.get('str_field') == 'test1'
        assert data.get('int_field') == 1

    @classmethod
    def test_model_list_load(cls):
        ''' Should serialize list of dicts into list of objects '''
        test_models = TestModel.load([cls.dict1, cls.dict2], many=True)
        assert test_models[0].str_field == 'test1'
        assert test_models[0].int_field == 1
        assert test_models[1].str_field == 'test2'
        assert test_models[1].int_field == 2

    @classmethod
    def test_model_list_loads(cls):
        ''' Should serialize list of json strs into list of objects '''
        test_models = TestModel.loads('[%s, %s]' % (cls.str1, cls.str2), many=True)
        assert test_models[0].str_field == 'test1'
        assert test_models[0].int_field == 1
        assert test_models[1].str_field == 'test2'
        assert test_models[1].int_field == 2

    @classmethod
    def test_model_list_dump(cls):
        ''' Should deserialize list of objects into list of dicts '''
        test_models = TestModel.load([cls.dict1, cls.dict2], many=True)
        assert TestModel.list_dump(test_models) == [cls.dict1, cls.dict2]

    @classmethod
    def test_model_list_dumps(cls):
        ''' Should deserialize list of objects into list of json strs '''
        test_models = TestModel.loads('[%s, %s]' % (cls.str1, cls.str2), many=True)
        data = json.loads(TestModel.list_dumps(test_models))
        assert data[0].get('str_field') in ['test1', 'test2']
        assert data[0].get('int_field') in [1, 2]
        assert data[1].get('str_field') in ['test1', 'test2']
        assert data[1].get('int_field') in [1, 2]

class TestUtils(TestCase):

    def test_encode_decode(self):
        ''' Should successfully encode and decode a string '''
        original_value = 'test_string'
        encoded_value = utils.encode('test_string')
        decoded_value = utils.decode(encoded_value)

        assert original_value == decoded_value
        assert original_value != encoded_value

class TestLogger(TestCase):

    def test_pcf_logger(self):
        ''' Should successfully use the pcf_logger at app.logging '''
        app = create_app()
        with self.assertLogs(pcf_logger) as cm:
            pcf_logger.handlers[0].setFormatter(formatter)
            pcf_logger.info('test')
            with app.test_request_context(
                        '/test_logger/', method='POST', data='{"test": "logger"}'):
                pcf_logger.warning('test with context')
        assert match(r'\[INFO\] \[.+\] test', cm.output[0]) is not None
        assert match(r'\[WARNING\] \[None\] \[None\] \[POST\] \[http://localhost/test_logger/\] \[b\'{"test": "logger"}\'\] \[.+\] test with context', cm.output[1]) is not None
