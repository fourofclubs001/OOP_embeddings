import torch
import torch.nn as nn

class ObjectEmbedding(nn.Module):
    def __init__(self, 
                 embedding_dim, 
                 colabs_int_size,
                 colabs_ext_size, 
                 output_size):
        super(ObjectEmbedding, self).__init__()

        #Cálculo input size
        #La entrada es la suma de:
        #1. Embedding <clase,método> --> embedding_dim
        #2. Embedding objeto receptor --> embedding_dim
        #3. Lista de embeddings de colabs internos --> n vectores
        #3. Lista de embeddings de colabs externos --> m vectores

        self.final_input_size = embedding_dim * (2 + colabs_ext_size + colabs_int_size)
        
        #Feed-Forward Multicapa
        self.final_rnn = nn.Sequential(
            nn.Linear(self.final_input_size, self.final_input_size // 2),
            nn.ReLU(),
            nn.Linear(self.final_input_size // 2, output_size)
        )

    def forward(self, 
                class_method,   # embedding <clase,metodo>
                recep_obj,      # embedding objeto receptor
                int_colabs,     # lista de embeddings de colaboradores internos 
                ext_colabs,     # lista de embeddings de colaboradores externos 
                ):
        
        # 1. Obtener el tamaño del batch
        batch_size = class_method.size(0)

        # 2. Aplanar (Flatten) los colaboradores
        # Transformamos de (Batch, N, Dim) a (Batch, N * Dim)
        # El -1 es para que PyTorch calcule la dimensión restante
        int_colabs_flat = int_colabs.reshape(batch_size, -1)
        ext_colabs_flat = ext_colabs.reshape(batch_size, -1)
        
        # 3. Concatenamos todo en un solo vector
        combined_vector = torch.cat([
            class_method,
            recep_obj,
            int_colabs_flat,
            ext_colabs_flat
        ], dim=1) 
        
        # combined_vector shape: (Batch, final_input_size)

        #3.5 PRUEBA
        # Tamaño real que construimos
        tamaño_real = combined_vector.size(1)
        
        # Comparamos con el tamaño teórico que calculamos en __init__
        if tamaño_real == self.final_input_size:
            print(f"EXITO: El vector combinado mide {tamaño_real}")
        else:
            print(f"ERROR: El vector mide {tamaño_real}, pero la red espera {self.final_input_size}.")


        # 4. Pasar por la Feed-Forward
        final_output = self.final_rnn(combined_vector)
        
        return final_output
    
    ##PRUEBA
    # Configuración
BATCH_SIZE = 2
EMB_DIM = 4         
NUM_INT = 3         # 3 colaboradores internos (3 * 4 = 12 nums)
NUM_EXT = 2         # 2 colaboradores externos (2 * 4 = 8 nums)
# Total esperado: 4 (class) + 4 (recep) + 12 (int) + 8 (ext) = 28

model = ObjectEmbedding(EMB_DIM, NUM_INT, NUM_EXT, output_size=1)

# Datos falsos
fake_class = torch.randn(BATCH_SIZE, EMB_DIM)
fake_recep = torch.randn(BATCH_SIZE, EMB_DIM)
fake_int = torch.randn(BATCH_SIZE, NUM_INT, EMB_DIM)
fake_ext = torch.randn(BATCH_SIZE, NUM_EXT, EMB_DIM)

print("\n--- Iniciando Forward Pass ---")
output = model(fake_class, fake_recep, fake_int, fake_ext)