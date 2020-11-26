##############
# Code validé
###############
library("reshape")
library("ggplot2")

#import data
DF <- read.table("metric/alexandria.csv", header=T, sep=',')

# convert data type
DF$taxid <- as.character(DF$taxid)

#reshape data
DF2 = melt(DF, id.vars="taxid")

#ggplot
ggplot(DF2, aes(x=variable, y=taxid, fill=value)) +
  scale_fill_gradientn(colours = plasma(100)) +
  ggtitle("Heatmap") +
  xlab("genes") + ylab("taxid") +
  geom_tile()

#resize ggplot
DF_resize = DF[1:30]

DF_resize2 = melt(DF_resize, id.vars="taxid")
ggplot(DF_resize2, aes(x=variable, y=taxid, fill=value)) +
  scale_fill_gradientn(colours = plasma(100)) +
  ggtitle("Heatmap") +
  xlab("genes") + ylab("taxid") +
  geom_tile()

######
# TEST
######
# Génération de données
DF1 <- data.frame(c(9606, 10029, 10036),
                  c(20, 56, 48),
                  c(0, 25, 89),
                  c(100, 56, 69),
                  c(72, 63, 42),
                  c(4, 14, NA),
                  c(42, 35, 12))
colnames(DF1) <- c("taxid", "X1", "X2", "X3", "X4", "X5", "X6")
DF1$taxid <- as.character(DF1$taxid)

DF2 = melt(DF1, id.vars=("taxid"))

ggplot(DF2, aes(x=variable, y=taxid, fill=value)) +
  scale_fill_gradientn(colours = plasma(100)) +
  ggtitle("Heatmap") +
  xlab("genes") + ylab("species") +
  geom_tile()

# essai avec une autre méthode
x <- LETTERS[1:20] # gene
y <- paste0("taxid", seq(1,3)) # taxid
DF1 <- expand.grid(X=x, Y=y)
DF1$Z <- sample(0:100, 20) # metric

DF2 = melt(DF1, id.vars=("Y"))
ggplot(DF2, aes(variable, taxid, value)) +
  geom_tile()
