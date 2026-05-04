import unittest
from pathlib import Path
from src.config import config

class TestConfig(unittest.TestCase):
    """Testes unitários para a classe de configuração."""

    def test_directories_creation(self):
        """Testa se os diretórios principais são criados corretamente."""
        config.setup_directories()
        
        self.assertTrue(config.MODELS_DIR.exists())
        self.assertTrue(config.OUTPUT_DIR.exists())

    def test_paths_are_valid(self):
        """Testa se as configurações de caminho estão referenciando os locais certos na raiz do repositório."""
        base_dir = config.BASE_DIR
        self.assertEqual(base_dir.name, "Magic_Animate")
        self.assertEqual(config.DENSEPOSE_DIR, base_dir / "detectron2")
        self.assertEqual(config.MAGIC_ANIMATE_DIR, base_dir / "magic-animate")

if __name__ == '__main__':
    unittest.main()
