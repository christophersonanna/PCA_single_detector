# -*- coding: utf-8 -*-

#Only step is processing the data from c through a PCA
#for now, we'll create a new PCA for the data, but I will need to account for 
#   when I need to apply new data to a pre-existing PCA

data_array = np.array(data)
pca = PCA(n_components=N_COMPONENTS_PCA)
transformed_data = pca.fit_transform(data_array)