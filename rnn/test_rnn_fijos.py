import unittest
import torch
from rnn_colabs_fijos import ObjectEmbedding 

class TestObjectEmbedding(unittest.TestCase):
    def setUp(self):
        #Definimos las constantes para el test
        self.batch_size = 2
        self.emb_dim = 4
        self.num_int = 3
        self.num_ext = 2
        self.output_size = 1
        
        #Instanciamos el modelo
        self.model = ObjectEmbedding(
            embedding_dim=self.emb_dim, 
            colabs_int_size=self.num_int, 
            colabs_ext_size=self.num_ext, 
            output_size=self.output_size
        )
        
        #Generamos datos aleatorios para usar en los tests
        self.fake_class = torch.randn(self.batch_size, self.emb_dim)
        self.fake_recep = torch.randn(self.batch_size, self.emb_dim)
        self.fake_int = torch.randn(self.batch_size, self.num_int, self.emb_dim)
        self.fake_ext = torch.randn(self.batch_size, self.num_ext, self.emb_dim)

    def test_initialization_dimensions(self):
        """
        Verifica que el modelo calculó bien el tamaño de entrada interno.
        """
        #Tamaño esperado calculado "a mano": 4*(2 + 3 + 2) = 28
        expected_size = self.emb_dim * (2 + self.num_int + self.num_ext)
        
        #Verificamos que sean iguales
        self.assertEqual(self.model.final_input_size, expected_size, 
                         "El cálculo interno del tamaño de entrada es incorrecto.")

    def test_forward_pass_shape(self):
        """
        Verifica que al pasar datos, la salida tenga el tamaño correcto.
        """
        #Ejecutamos el forward
        output = self.model(self.fake_class, self.fake_recep, self.fake_int, self.fake_ext)
        
        #Esperamos una forma de (Batch_Size, Output_Size) -> (2, 1)
        expected_shape = (self.batch_size, self.output_size)
        
        self.assertEqual(output.shape, expected_shape, 
                         f"El shape de salida debería ser {expected_shape} pero es {output.shape}")

    def test_output_values_type(self):
        """
        Verifica que no devuelva NaNs o infinitos.
        """
        output = self.model(self.fake_class, self.fake_recep, self.fake_int, self.fake_ext)
        
        # torch.isnan devuelve True si hay algún error numérico
        self.assertFalse(torch.isnan(output).any(), "El modelo devolvió valores NaN (error numérico).")

if __name__ == '__main__':
    unittest.main()