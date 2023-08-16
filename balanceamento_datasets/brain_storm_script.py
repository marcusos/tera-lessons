# test_df[test_df.default == 1][['term', 'total_loan', 'installment', 'loan_amnt', 'total_pymnt', 'recoveries', 'ead', 'ead_ratio', 'lgd_ratio', 'losses']]
# Não entendi pq installments * term é diferente do total_pymnt
# Porém, o loan_amnt * int_rate é igual ao total_pymnt


from scipy.optimize import minimize
from numpy.random import rand

# LOAN variables
loan_amnt = 20000
loan_fees = 0.01

#CONTRAINTS
min_ir = 0.075
max_ir = 0.30

# RISK variables
risk = 'C'
default_prob = policy_3.loc[policy_3.risk_category == risk, 'default_ratio'].item()
EAD = policy_3.loc[policy_3.risk_category == risk, 'EAD'].item()
LGD = policy_3.loc[policy_3.risk_category == risk, 'LGD'].item()
EAD_LGD = EAD*LGD
term_months = 36
term_years = term_months/12

# term will have an effect on the probability of default, also on the EAD/LGD
def compute_roi(int_rate, loan_amnt, default_prob, EAD_LGD, loan_fees, term):
    principal = (1 + int_rate)*loan_amnt
    expected_loss = principal*EAD_LGD*default_prob
    profit = (int_rate*loan_amnt)
    net_profit = profit - expected_loss - loan_fees*loan_amnt
    ROI = net_profit/loan_amnt
    ROI_annualized = ROI/term

    return ROI, ROI_annualized, principal, expected_loss, profit, net_profit

def objective(int_rate, *args):
    return compute_roi(int_rate, *args)[0]

def c1(int_rate, *args):
    'Land area constraint'
    roi_annualized = compute_roi(int_rate, *args)[1]
    return (roi_annualized - 0.025)

args=(loan_amnt, default_prob, EAD_LGD, loan_fees, term_years)
# define the starting point as a random sample from the domain
pt = min_ir + rand() * (max_ir - min_ir)

constraints = [{'type': 'ineq', 'fun': c1, 'args': args}]

#result = minimize(compute_roi, pt, method='L-BFGS-B', args=args, cons'raints=constraints)
result = minimize(objective, pt, args=args, constraints=constraints)

# Testando
#print(pt)

best_int_rate = float(result.x[0])

roi_result = compute_roi(best_int_rate, *args)
roi_result_labels = ['ROI', 'ROI_annualized', 'principal', 'expected_loss', 'profit', 'net_profit']
roi_result = dict(zip(roi_result_labels, list(roi_result)))

print('Best interest rate', best_int_rate)
print('Roi result:', roi_result)


# COLOR PALLET
sns.set(style="ticks", context="talk")
plt.style.use(['dark_background'])

color_pallet = ("#6A38D4",) + plt_io.templates["custom_dark"]['layout']['colorway']

gray_label_bg = '#E0E0E0'
plt.rcParams.update({"grid.linewidth":0.5, "grid.alpha":0.5, "lines.linewidth": 1.5, "xtick.labelsize": 11, "ytick.labelsize": 11, "font.size": 14,
                     "axes.labelsize": 15,
                     "xtick.color": gray_label_bg,
                     "ytick.color": gray_label_bg,
                     "axes.facecolor": '#121212',
                     "axes.edgecolor" : gray_label_bg,
                     "axes.labelcolor" : gray_label_bg,
                     "figure.facecolor" : '#121212',
                     #figure.edgecolor
                     "axes.axisbelow": 'false',
                     "axes.linewidth": 0.8,
                     "xtick.major.bottom": "true",
                     })