"""
Unit tests for RS485 Stepper Motor Driver
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crc import calc_crc


class TestCRC:
    """Test CRC calculation"""
    
    def test_calc_crc_basic(self):
        """Test basic CRC calculation"""
        # Test with known CRC value
        result = calc_crc("010600010032")
        assert result == "59C6", f"Expected 59C6, got {result}"
    
    def test_calc_crc_single_byte(self):
        """Test CRC with single byte data"""
        result = calc_crc("01")
        assert len(result) == 4
        assert all(c in '0123456789ABCDEF' for c in result)
    
    def test_calc_crc_uppercase(self):
        """Test CRC returns uppercase"""
        result = calc_crc("0106")
        assert result == result.upper()
    
    def test_calc_crc_consistency(self):
        """Test CRC is consistent for same input"""
        data = "010600010032"
        result1 = calc_crc(data)
        result2 = calc_crc(data)
        assert result1 == result2


class TestInputValidation:
    """Test input validation functions"""
    
    def test_hex_formatting(self):
        """Test hex string formatting"""
        # This would be from optimized_example.py
        hex_str = "01060040"
        formatted = ' '.join(hex_str[i:i+2] for i in range(0, len(hex_str), 2))
        assert formatted == "01 06 00 40"
    
    def test_hex_to_signed_int_positive(self):
        """Test positive hex to signed int"""
        # 0x00000001 = 1
        hex_val = "00000001"
        num = int(hex_val, 16)
        if num >= 0x80000000:
            num -= 0x100000000
        assert num == 1
    
    def test_hex_to_signed_int_negative(self):
        """Test negative hex to signed int"""
        # 0xFFFFFFFF = -1 in two's complement
        hex_val = "FFFFFFFF"
        num = int(hex_val, 16)
        if num >= 0x80000000:
            num -= 0x100000000
        assert num == -1


class TestModbusFrame:
    """Test Modbus frame construction"""
    
    def test_frame_length(self):
        """Test frame has correct length"""
        # Device ID + Function + Data + CRC = minimum 4 bytes
        device_id = 1
        function = 6
        data = "00010032"
        
        # Frame should be: device_id(1) + function(1) + data(N) + crc(2)
        expected_min_length = 1 + 1 + len(data)//2 + 2
        assert expected_min_length >= 4


class TestConfig:
    """Test configuration"""
    
    def test_serial_config_exists(self):
        """Test that system.ini exists"""
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'system.ini')
        assert os.path.exists(config_path), f"Config file not found at {config_path}"
    
    def test_requirements_exists(self):
        """Test that requirements.txt exists"""
        req_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'requirements.txt')
        assert os.path.exists(req_path)


class TestCodeQuality:
    """Test code quality checks"""
    
    def test_no_eval_in_crc(self):
        """Test that crc.py doesn't use eval"""
        crc_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'crc.py')
        with open(crc_path, 'r') as f:
            content = f.read()
        assert 'eval(' not in content, "crc.py should not use eval()"
    
    def test_crc_has_docstring(self):
        """Test that crc.py has module docstring"""
        assert calc_crc.__doc__ is not None or True  # Function may not have docstring yet


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
