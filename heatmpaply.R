# G?n?ration de donn?es
DF <-  data.frame(replicate(10, sample(0:100, 10, rep=TRUE)))
rownames(DF) <- paste("species", as.character(1:10), sep="")
colnames(DF) <- c(1:10)#paste("gene", as.character(1:100), sep="")

D1 <- read.table("data9606.csv", header=F, sep=',')
D2 <- read.table("data10020.csv", header=F, sep=',')

D <- D1[1,]
D <- rbind(D1, D2[1,])

DF <- read.table("metric/alexandria.csv", header=T, sep=',')

## force value for exemple
DF$"1"[1] = 0
DF$"1"[2] = 100
DF$"1"[3] = NA

DF2 <- data.matrix(DF)

# heatmap
myColor <- colorRampPalette(c("white", "purple4")) # low to hight

heatmap(DF2, col=myColor(n = 1000))



# avec ggplot2
library("reshape")
library("ggplot2")
library("viridis")

DF3 <- melt(DF2)
head(DF3)

ggp <- ggplot(DF3, aes(X2, X1)) +
  geom_tile(aes(fill = value)) +
  #scale_fill_gradient(low = "white", high = "purple4")
  scale_fill_gradientn(colours = plasma(100)) +
  ggtitle("Le graph de la mort qui tue") +
  xlab("genes") + ylab("species")
ggp


# avec heatmap.2
library("heatmaply")
library("dendextend")
# dendrogramme pour les lignes
row_dend <- DF %>%
  dist() %>%
  hclust() %>%
  as.dendrogram() %>%
  set("branches_lwd", 1) %>%
  set("branches_k_color", c("#2E9FDF", "#00AFBB", "#E7B800", "#FC4E07"), k = 4)
# text custom
mat <- DF2
mat[] <- paste("Odd tell you that", rownames(mat))
mat[] <- lapply(colnames(mat), function(colname) {
  paste0(mat[, colname], " and gene ", colname)
})
# annotation avec un autre facteur
x <- as.matrix(DF)
anno <- colorspace::rainbow_hcl(nrow(x))
# graph
heatmaply(
  DF2,
  seriate = "OLO", # OLO arrangement optimale des feuilles, mean résultat par défaut du package gplot::heatmap et none dendrogrammes sans rotation
  colors = myColor(100),
  column_text_angle = 0,
  plot_method = "ggplot",
  Rowv = row_dend,
  Colv = NULL,
  xlab = "gene",
  #ylab = "espèce",
  main = "La Heatmap by Odd",
  #showticklabels = c(T,F), # un truc pour les NA
  RowSideColors = anno, # pour ajouter une annotation de couleur en plus on peut mettre autant de facteur dans cette partie
  cellnote = DF2,
  custom_hovertext = mat,
  file = "heatmaply_plot.html" # ou png mais il faudra peut-être orca
)

