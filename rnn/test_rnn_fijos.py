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
        Verifica que el modelo calcule bien el tamaño de entrada interno
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

    def test_internal_padding_logic(self):
        """
        Verifica que la función interna fill_list haga bien el padding y truncado
        """
        # Max int es 3 (self.num_int)
        
        # Caso 1: Lista corta (1 elemento), deberia agregar 2 filas de ceros
        vec_corto = torch.ones(1, self.emb_dim)
        
        # Caso 2: Lista larga (5 elementos), deberia cortar los últimos 2
        vec_largo = torch.ones(5, self.emb_dim) * 5
        
        # Caso 3: Lista vacía. Debería devolver 3 filas de ceros.
        vec_vacio = torch.empty(0, self.emb_dim)
        
        # Armamos el batch (lista de tensores)
        batch_listas = [vec_corto, vec_largo, vec_vacio]
        
        # Llamamos a la función interna del modelo
        padded_tensor = self.model.fill_list(batch_listas, max_len=self.num_int)
        
        # --- VERIFICACIONES ---
        
        # 1. Chequeamos dimensiones: (Batch=3, Max=3, Dim=4)
        expected_shape = (3, self.num_int, self.emb_dim)
        self.assertEqual(padded_tensor.shape, expected_shape, 
                         f"El shape del padding falló. Se esperaba {expected_shape}, se obtuvo {padded_tensor.shape}")
        
        # 2. Chequeamos el Relleno (Caso Corto)
        # La fila 0 debe ser unos, las filas 1 y 2 deben ser ceros
        self.assertTrue(torch.equal(padded_tensor[0, 0], torch.ones(self.emb_dim)), "Falló al mantener el dato original")
        self.assertTrue(torch.equal(padded_tensor[0, 1:], torch.zeros(2, self.emb_dim)), "Falló al rellenar con ceros")

        # 3. Chequeamos el Truncado (Caso Largo)
        # Debería tener solo 3 filas, y todas con valor 5
        self.assertTrue(torch.equal(padded_tensor[1], torch.ones(3, self.emb_dim) * 5), "Falló al truncar la lista larga")

        # 4. Chequeamos Vacío
        # Todo debe ser cero
        self.assertTrue(torch.equal(padded_tensor[2], torch.zeros(3, self.emb_dim)), "Falló al manejar lista vacía")

    def test_forward_variable_input(self):
        """
        Verifica que el forward completo funcione con un batch con longitudes variables
        """
        # Creamos un batch de 2 instancias con tamaños distintos
        
        # Instancia 1: 1 interno, 0 externos
        i1_int = torch.randn(1, self.emb_dim)
        i1_ext = torch.empty(0, self.emb_dim)
        
        # Instancia 2: 4 internos (se pasa del max 3), 1 externo
        i2_int = torch.randn(4, self.emb_dim)
        i2_ext = torch.randn(1, self.emb_dim)
        
        # Listas para el forward
        list_int = [i1_int, i2_int]
        list_ext = [i1_ext, i2_ext]
        
        # inputs fijos (clase y receptor) para batch de 2
        cm = torch.randn(2, self.emb_dim)
        ro = torch.randn(2, self.emb_dim)
        
        # Ejecutamos forward. Si el padding anda mal, da error de dimensiones
        try:
            output = self.model(cm, ro, list_int, list_ext)
        except RuntimeError as e:
            self.fail(f"El forward falló con listas variables: {e}")
            
        # Verificamos shape de salida
        self.assertEqual(output.shape, (2, self.output_size))

if __name__ == '__main__':
    unittest.main()