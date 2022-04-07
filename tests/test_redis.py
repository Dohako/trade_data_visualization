from loguru import logger
from container_way.generator.data_handler import MyRedis as GRedis
from container_way.view_point.utils.redis_handler import MyRedis as VRedis
import dotenv
import pytest
from tests.tredis import TRedis

def test_00_redis_empty_env():
    """
    Testing env error so it couldn't run without env vars for redis
    """
    with pytest.raises(ValueError):
        GRedis()
        VRedis()

    dotenv.load_dotenv(dotenv_path='./tests/test.env')

def test_01_redis_funcs_in_generator():
    """
    Testing main redis features in generator
    """
    r = GRedis()
    r.my_r = TRedis()

    current_key = "test_1"
    first_val = 1
    second_val = 2
    third_val = "3"

    check = r.update_redis(current_key, first_val)
    assert check == 1, "Should return 1, because added one item"

    check = r.update_redis(current_key, second_val)
    assert check == 2, "Should return 2, because added one item"

    check = r.get_last_value("test_1")
    assert check == second_val, f"val {second_val} was last to input, so need to be first to output"

    
    with pytest.raises(ValueError):
        r.update_redis(current_key, third_val) # last value was not int
    

def test_02_redis_funcs_in_view():
    """
    Testing main redis features in view_point
    """
    r = VRedis()
    r.my_r = TRedis()

    current_key = "test_1"
    first_val = [1,2,3]
    test_from = 2
    test_minus_from = -2

    with pytest.raises(ValueError):
        r.get_list_from_redis(current_key)

    r.my_r.global_redis_dict.update({current_key:first_val})

    result = r.get_list_from_redis(current_key)
    assert result == first_val, "result should be empty on start"

    result = r.get_list_from_redis(current_key, test_from)
    assert result == first_val[test_from:], f"Should return elements from {test_from}"

    result = r.get_list_from_redis(current_key, test_minus_from)
    assert result == first_val[test_minus_from:], f"Should return elements from {test_minus_from}"

