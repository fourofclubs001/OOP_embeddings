import torch
import torch.nn as nn

class ObjectEmbedding(nn.Module):
    def __init__(self, 
                 embedding_dim, 
                 colabs_int_size, #long maxima de colabs internos
                 colabs_ext_size, #long maxima de colabs externos
                 output_size):
        super(ObjectEmbedding, self).__init__()

        self.emb_dim = embedding_dim
        self.max_int = colabs_int_size
        self.max_ext = colabs_ext_size

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

    def fill_list(self, batch_listas, max_len):
        """
        Recibe batch de listas y completa cada una con padding para alcanzar longitud max_len
        """
        batch_completo=[]
        
        for lista in batch_listas:
            len_actual= lista.size(0)  #Cantidad de colaboradores

            #Si faltan colaboradores
            if len_actual < max_len:
                ceros = torch.zeros(max_len-len_actual, self.emb_dim).to(lista.device)
                if len_actual==0:
                    padded=ceros #Si la lista estaba vacia, es todo ceros
                else:
                    padded= torch.cat([lista,ceros],dim=0) # Si no, concatenamos con los ceros

            #Si sobran colaboradores
            elif len_actual>max_len:
                padded= lista[:max_len,:] #Truncamos
            else: #Si era del tamaño correcto
                padded= lista
            
            batch_completo.append(padded)
            
        return torch.stack(batch_completo)

    def forward(self, 
                class_method,   # embedding <clase,metodo>
                recep_obj,      # embedding objeto receptor
                list_int_colabs,     # lista de embeddings de colaboradores internos 
                list_ext_colabs,     # lista de embeddings de colaboradores externos 
                ):
        
        #1. Aplicamos el padding para obtener tensores fijos
        tensor_int = self.fill_list(list_int_colabs, self.max_int)
        tensor_ext = self.fill_list(list_ext_colabs, self.max_ext)
        
        # 2. Obtenemos el tamaño del batch
        batch_size = class_method.size(0)

        # 3. Aplanar (Flatten) los colaboradores
        # Transformamos de (Batch, N, Dim) a (Batch, N * Dim)
        # El -1 es para que PyTorch calcule la dimensión restante
        int_colabs_flat = tensor_int.reshape(batch_size, -1)
        ext_colabs_flat = tensor_ext.reshape(batch_size, -1)
        
        # 3. Concatenamos todo en un solo vector
        combined_vector = torch.cat([
            class_method,
            recep_obj,
            int_colabs_flat,
            ext_colabs_flat
        ], dim=1) 
        
        # 4. Pasar por la Feed-Forward
        final_output = self.final_rnn(combined_vector)
        
        return final_output
