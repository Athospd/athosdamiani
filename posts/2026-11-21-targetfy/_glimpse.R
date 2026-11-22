# Draws the post's tar_glimpse() graphs from the real pipeline.
# Run in a folder holding the post's _targets.R, R/analysis_functions.R and
# data/sales.csv (from targetfy's tests/fixtures/sales), after tar_make().
# Screenshot the HTML with headless Chrome (--force-device-scale-factor=2), then crop:
# glimpse_light.html -> glimpse.png (post), glimpse_dark.html -> _glimpse-dark.png (thumbnail).
library(targets)
save <- function(w, file, h, dark) {
  w$width <- "100%"; w$height <- paste0(h, "px")
  w$x$legend <- NULL
  w <- visNetwork::visNodes(w, font = list(size = 18, color = if (dark) "#cfd5dc" else "#343434"))
  w <- visNetwork::visInteraction(w, dragView = FALSE, zoomView = FALSE)
  htmlwidgets::saveWidget(w, file, selfcontained = FALSE, libdir = "lib",
                          background = if (dark) "#12161b" else "white")
}
g <- tar_glimpse()
save(g, "glimpse_dark.html", 260, TRUE)
save(g, "glimpse_light.html", 220, FALSE)
