"""
测试文件 - 知识库服务测试
"""
import pytest
import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from knowledge_base import KnowledgeBaseService, get_string_md5, check_md5, save_md5


class TestMD5Functions:
    """MD5相关函数测试"""
    
    def test_get_string_md5(self):
        """测试MD5计算"""
        md5 = get_string_md5("测试字符串")
        assert len(md5) == 32
        assert isinstance(md5, str)
    
    def test_check_md5_new(self, tmp_path):
        """测试检查新MD5"""
        import config_data as config
        # 临时修改MD5文件路径
        original_path = config.md5_path
        config.md5_path = str(tmp_path / "test_md5.txt")
        
        try:
            assert not check_md5("test_md5_123")
        finally:
            config.md5_path = original_path
    
    def test_save_and_check_md5(self, tmp_path):
        """测试保存和检查MD5"""
        import config_data as config
        original_path = config.md5_path
        config.md5_path = str(tmp_path / "test_md5.txt")
        
        try:
            test_md5 = "test_md5_456"
            save_md5(test_md5)
            assert check_md5(test_md5)
        finally:
            config.md5_path = original_path


class TestKnowledgeBaseService:
    """知识库服务测试"""
    
    @pytest.fixture
    def service(self, tmp_path):
        """创建测试服务实例"""
        import config_data as config
        # 临时修改存储路径
        original_dir = config.persist_directory
        config.persist_directory = str(tmp_path / "chroma_test")
        
        try:
            return KnowledgeBaseService()
        finally:
            config.persist_directory = original_dir
    
    def test_service_initialization(self, service):
        """测试服务初始化"""
        assert service is not None
        assert hasattr(service, 'chroma')
        assert hasattr(service, 'spliter')
    
    def test_upload_by_str_success(self, service):
        """测试成功上传"""
        result = service.upload_by_str("测试内容123", "test_file.txt")
        assert "[成功]" in result
    
    def test_upload_duplicate(self, service):
        """测试重复上传"""
        content = "重复内容测试"
        result1 = service.upload_by_str(content, "file1.txt")
        assert "[成功]" in result1
        
        result2 = service.upload_by_str(content, "file2.txt")
        assert "[跳过]" in result2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
