"""
a_mu
===
The a_mu VLL interpretation diagram.
"""
import matplotlib.pyplot as plt
from feynman import Diagram

fig = plt.figure(figsize=(10.,10.))
ax = fig.add_axes([0,0,1,1], frameon=False)

diagram = Diagram(ax)
leftpoint = diagram.vertex(xy=(.1,.6), marker='')
muchi1 = diagram.vertex(xy=(.3,.6))
muchi2 = diagram.vertex(xy=(.7,.6))
chichigamma = diagram.vertex(xy=(.5,.6))
rightpoint = diagram.vertex(xy=(.9,.6), marker='')
bottompoint = diagram.vertex(xy=(.5,.2), marker='')

mu1 = diagram.line(leftpoint, muchi1, arrow=True)
chi1 = diagram.line(muchi1, chichigamma, arrow=True)
chi2 = diagram.line(chichigamma, muchi2, arrow=True)
mu2 = diagram.line(muchi2, rightpoint, arrow=True)
gamma = diagram.line(chichigamma, bottompoint, style='wiggly', amplitude=0.02)
Z = diagram.line(muchi1, muchi2, style='wiggly elliptic', amplitude=0.02)

mu1.text(r"$\mu$",fontsize=30)
mu2.text(r"$\mu$",fontsize=30)
chi1.text(r"$\chi$",fontsize=30)
chi2.text(r"$\chi$",fontsize=30)
gamma.text(r"$\gamma$",fontsize=30)
Z.text(r"$Z$",fontsize=30)

diagram.plot()
plt.savefig('a_mu.png', dpi=300)