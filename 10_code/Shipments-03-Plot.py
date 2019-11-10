# Pre-Post plot
import pandas as pd
import numpy as np
from plotnine import *

# Pre-post plot for FL
FL_prePost = (ggplot(shipment_FL_grouped,aes(x = 'YEAR', y = 'QUANTITY_PERCAP', group = 'POST'))
 + geom_point(alpha = 0.5)
 + geom_smooth(method='lm', fill=None, colour="red")
 +theme_classic(base_family = "Helvetica")
 +labs(title="opioid shipments Pre-Post analysis for Florida",
       x="Year",
       y="Quantity Per Cap"))

FL_prePost.save('/Users/ZifanPeng/Desktop/estimating-impact-of-opioid-prescription-regulations-team-2/30_results/FL-PrePost.png')
