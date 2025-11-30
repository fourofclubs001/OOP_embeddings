import torch
import torch.nn as nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

class ObjectEmbedding(nn.Module):
    def __init__(self, embedding_dim, hidden_size, output_size):
        super(ObjectEmbedding, self).__init__()

        #Red recurrente Colabs Internos (GRU)
        self.gru_int= nn.GRU(input_size=embedding_dim,
                             hidden_size=hidden_size,
                             batch_first=True
        )
        #Red recurrente Colabs Externos (GRU)
        self.gru_ext= nn.GRU(input_size=embedding_dim,
                             hidden_size=hidden_size,
                             batch_first=True
        )

        #Feed-Forward Multicapa
        final_input_size = embedding_dim * 2 + hidden_size * 2
        
        self.final_rnn = nn.Sequential(
            nn.Linear(final_input_size, final_input_size // 2),
            nn.ReLU(),
            nn.Linear(final_input_size // 2, output_size)
        )

    def forward(self, 
                class_method,   # embedding <clase,metodo>
                recep_obj,      # embedding objeto receptor
                int_colabs,     # lista de embeddings de colaboradores internos -> TENSOR CON PADDING
                int_colabs_lengths, # lista con los tamanios de las listas de colabs internos de este batch
                ext_colabs,     # lista de embeddings de colaboradores externos -> TENSOR CON PADDING
                ext_colabs_lengths  # lista con los tamanios de las listas de colabs internos de este batch
                ):
        
        # Procesamiento de Colaboradores Internos (int_colabs)
        
        # a. Empaquetar (Pack)
        # Le decimos a PyTorch que ignore el padding
        # enforce_sorted=False para no tener que ordenar el batch
        packed_int_input = pack_padded_sequence(
            int_colabs, 
            int_colabs_lengths.cpu(), #las longitudes deben estar en la cpu 
            batch_first=True, 
            enforce_sorted=False
        )
        
        # b. Pasar por la GRU
        # El 'hidden_int' que devuelve ignora el padding.
        # No necesitamos la salida 'outputs_int'
        _, hidden_int = self.gru_int(packed_int_input)
        
        # c. Obtener el estado oculto final
        final_hidden_int = hidden_int[-1, :, :]
        
        # Procesamiento de Colaboradores Externos (ext_colabs)
        
        # a. Empaquetar
        packed_ext_input = pack_padded_sequence(
            ext_colabs, 
            ext_colabs_lengths.cpu(), 
            batch_first=True, 
            enforce_sorted=False
        )
        
        # b. Pasar por la GRU
        _, hidden_ext = self.gru_ext(packed_ext_input)
        
        # c. Obtener el estado oculto final
        final_hidden_ext = hidden_ext[-1, :, :]
        
        # Concatenamos todo lo de antes
        
        combined_vector = torch.cat([
            class_method,
            recep_obj,
            final_hidden_int,
            final_hidden_ext
        ], dim=1) 
        
        final_output = self.final_rnn(combined_vector)
        
        return final_output