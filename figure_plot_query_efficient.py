import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

# Load merged data
df = pd.read_csv('results/query_efficient_merged_summary_softmax.csv')

# Set Seaborn theme with elegant aesthetics
sns.set_theme(style="whitegrid")

# Use Seaborn "Set2" color palette for a soft, distinct, and aesthetic look
palette = sns.color_palette("Set2")  # Set2 has pastel yet distinguishable colors
#palette = ["Purple", "Green", "Red", "Blue"]
colors = {'BestN_min': palette[0], 'BestN_softmax': palette[1], 
          'Latent_min': palette[2], 'Latent_softmax': palette[3]}

# Elegant marker choices
markers = {'BestN_min': 'o', 'BestN_softmax': 's', 
           'Latent_min': '^', 'Latent_softmax': 'D'}

label_names = {'BestN_min': 'GuideRaw-H', 'BestN_softmax': 'GuideRaw-S', 
              'Latent_min': 'LEAD-H', 'Latent_softmax': 'LEAD-S'}

# Elegant marker choices
linestyles = {'BestN_min': '--', 'BestN_softmax': ':', 
           'Latent_min': '-', 'Latent_softmax': '-.'}

def split_score_variance(value):
    """Split string like '0.85±0.02' into mean and variance"""
    score, variance = value.split('±')
    return float(score), float(variance)

# Function to plot data beautifully
def plot_property(ax, property_name, title, is_legend=False):
    for method_agg in ['BestN_min', 'BestN_softmax', 'Latent_min', 'Latent_softmax']:
        method, agg = method_agg.split('_')
        mask = (df['method'] == method) & (df['opt_type'] == agg) & (df['property'] == property_name)
        
        # Select first 5 and last data points
        data = pd.concat([
            df[mask].sort_values('start_iter').head(5),
            df[mask].sort_values('start_iter').tail(1)
        ]).drop_duplicates()

        # Define column name
        column_name = 'pred_ddg' if property_name == 'ddg' else 'hydro'
        
        # Extract scores and variances
        scores, variances = zip(*[split_score_variance(val) for val in data[column_name]])
        scores, variances = np.array(scores), np.array(variances)
        
        # Plot line and points with Set2 colors
        ax.plot(data['start_iter'], scores, label=label_names[method_agg], color=colors[method_agg], linestyle=linestyles[method_agg],
                marker=markers[method_agg], linewidth=3, markersize=12, alpha=0.8)

        # Error bars for variance display (without shadow)
        ax.errorbar(data['start_iter'], scores, yerr=variances, fmt='none', 
                    color=colors[method_agg], capsize=8, capthick=2.5, elinewidth=2.5, alpha=0.8)

    # Set x-axis to log2 scale
    ax.set_xscale('log', base=2)
    ax.set_xticks([2**i for i in range(6)])
    ax.set_xticklabels([f"$2^{i}$" for i in range(6)], fontsize=20)
    for label in ax.get_yticklabels():
        label.set_fontsize(20)


    ax.set_xlabel('# Queries per Time Step', fontsize=20)
    ylabel = r'Predicted $\Delta \Delta G$' if property_name == 'ddg' else 'Hydropathy Score'
    ax.set_ylabel(ylabel, fontsize=20)
    
    #ax.set_title(title, fontsize=22, pad=12, color='#333333')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.tick_params(axis='both', which='major', labelsize=20)   
    if is_legend:   
        legend = ax.legend(fontsize=18, loc='best')


# Create figure and subplots
fig, ax = plt.subplots(figsize=(7.5, 6))
plot_property(ax, 'ddg', r' $\Delta \Delta G$ vs. # Queries per Time Step')
plt.tight_layout()
plt.savefig('results/query_efficient_comparison_ddg.pdf', bbox_inches='tight')
plt.clf()
fig, ax = plt.subplots(figsize=(7.5, 6))
plot_property(ax, 'hydro', 'Hydropathy Score vs. # Queries per Time Step', is_legend=True)
plt.savefig('results/query_efficient_comparison_hydro.pdf', bbox_inches='tight')
plt.close()

# Adjust layout and save figure

