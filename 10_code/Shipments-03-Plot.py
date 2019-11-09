# Pre-Post plot
import pandas as pd
import numpy as np
from plotnine import *

# Pre-post plot for FL
(ggplot(shipment_FL_grouped,aes(x = 'YEAR', y = 'QUANTITY_PERCAP', group = 'POST'))
 + geom_point()
 + geom_smooth(method='lm', fill=None, colour="red")
 +theme_classic(base_family = "Helvetica")
 +labs(title="opioid shipments pre-post analysis for Florida",
       x="Year",
       y="Quantity Per Cap"))
