from skimage import data, segmentation, color
from skimage.future import graph
from matplotlib import pyplot as plt


img = data.astronaut()
out0 = img

labels1 = segmentation.slic(img, compactness=30, n_segments=200)
out1 = color.label2rgb(labels1, img, kind='avg')

g = graph.rag_mean_color(img, labels1, mode='similarity')
labels2 = graph.cut_normalized(labels1, g)
out2 = color.label2rgb(labels2, img, kind='avg')

fig, ax = plt.subplots(ncols=3, sharex=True, sharey=True, figsize=(5, 3))

ax[0].imshow(out0)
ax[1].imshow(out1)
ax[2].imshow(out2)

for a in ax:
    a.axis('off')

plt.tight_layout()
plt.savefig('scikit-ncut.png', orientation='landscape')
plt.show()
