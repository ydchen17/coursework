plot.new()

plot.window(xlim = c(xlower,xupper), ylim = c(0.5,length(estimates)))

axis(side = 1, at = seq(xlower,xupper,0.5), labels = seq(xlower,xupper,0.5), cex.axis = 1.25)
axis(side = 2, at = seq(1,length(estimates)), labels = rev(type_names), las = 2)

mtext(strsplit(types[a], ".bed")[[1]][1], side = 3, line = 1, cex = 1.5)
mtext("Odds ratio relative to matched", side = 1, line = 2.5, cex = 1.25)

abline(v = 1, col = rgb(0,158,115,maxColorValue = 255), lwd = 2, lty = 'dashed')

position<-length(estimates) - x + 1
lines(x = c(estimates[x], estimates[x]), y = c((position - 0.1), (position + 0.1)), lwd = 3, col = rgb(rgb_colors[(x*3)-2],rgb_colors[(x*3)-1],rgb_colors[(x*3)],maxColorValue = 255))
lines(x = c(lower_bounds[x], upper_bounds[x]), y = c(position, position), lwd = 3, col = rgb(rgb_colors[(x*3)-2],rgb_colors[(x*3)-1],rgb_colors[(x*3)],maxColorValue = 255))
  
