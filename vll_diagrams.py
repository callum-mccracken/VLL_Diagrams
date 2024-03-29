"""
vll_diagrams
===
Makes VLL decay chain diagrams

- VLLs are produced by some boson, in pairs
- each VLL is either neutral or charged
- VLLs decay to either W, Z, or H
- Allowed decays of bosons: 
    W -> q q
    W -> l nu
    Z -> q q
    Z -> l l
    Z -> nu nu
    H -> q q
    H -> gamma gamma
    H -> Zqq Zqq, Zqq Zll, Zqq Znunu, Zll Zll, Zll Znunu, Znunu Znunu
    H -> Wqq Wqq, Wqq Wlnu, Wlnu Wlnu
    H -> l l 
    H -> g g

"""
import matplotlib.pyplot as plt
from feynman import Diagram

ew_boson_kwargs = {'style': 'wiggly', 'nwiggles': 5, 'amplitude': 0.02}
higgs_kwargs = {'style': 'dashed', 'arrow': False}
# for some reason the gluons are still wacky
gluon_kwargs = {'style': 'loopy', 'nloops': 2, 'arrow': False, 'amplitude': 0.005}
fermion_kwargs = {'arrow': True}

boson_decay_products = {
    r'$W$': [
        (r'$q$', r'$q$'),
        (r'$\ell$', r'$\nu$')
        ],
    r'$Z$': [
        (r'$q$', r'$q$'),
        (r'$\ell$', r'$\ell$'),
        (r'$\nu$', r'$\nu$')
        ],
    r'$H$': [
        (r'$\ell$', r'$\ell$'),
        (r'$g$', r'$g$'),
        (r'$q$', r'$q$'),
        (r'$\gamma$', r'$\gamma$'),
        (r'$Zqq$', r'$Zqq$'),
        (r'$Zqq$', r'$Z\ell\ell$'),
        (r'$Zqq$', r'$Z\nu\nu$'),
        (r'$Z\ell\ell$', r'$Z\ell\ell$'),
        (r'$Z\ell\ell$', r'$Z\nu\nu$'),
        (r'$Wqq$', r'$Wqq$'),
        (r'$Wqq$', r'$W\ell\nu$'),
        (r'$W\ell\nu$', r'$W\ell\nu$'),
        ]
}

#vll_labels = [r"$\tau'$", r"$\nu_{\tau'}$", r"$\mu'$", r"$\nu_{\mu'}$", r"$e'$", r"$\nu_{e'}$"]
vll_labels = [r"$\ell'$", r"$\nu'$"]
#fermion_labels = [r'$\tau$', r'$\nu_{\tau}$', r'$\mu$', r'$\nu_{\mu}$', r'$e$', r'$\nu_{e}$', r'$q$', r'$b$', r'$\nu$']
fermion_labels = [r'$\ell$', r'$\nu$', r'$q$', r'$b$']
ew_boson_labels = [r'$Z$', r'$Zqq$', r'$Z\ell\ell$', r'$Z\nu\nu$', r'$W$', r'$Wqq$', r'$W\ell\nu$', r'$\gamma$']
vll_decay_boson_labels = [r'$Z$', r'$W$', r'$H$']
gluon_labels = [r'$g$']
higgs_labels = [r'$H$']

middle_boson_labels = [r'$Z^{*}$ \\ $W^{*}$ \\ $\gamma^{*}$']


def get_kwargs(particle_label):
    """keyword arguments for plotting each kind of particle"""
    if particle_label in fermion_labels:
        return fermion_kwargs
    elif particle_label in ew_boson_labels:
        return ew_boson_kwargs
    elif particle_label in gluon_labels:
        return gluon_kwargs
    elif particle_label in higgs_labels:
        return higgs_kwargs
    elif particle_label in vll_labels:
        return fermion_kwargs
    else:
        raise ValueError('particle type not recognized: ' + particle_label)

def get_corresponding_lepton(vll, boson):
    """if you have a VLL decaying to a boson + lepton, find lepton"""
    assert vll in vll_labels
    #if r"\tau" in vll:
    #    flavour = r"\tau"
    #elif r"\mu" in vll:
    #    flavour = r'\mu'
    #else:
    #    flavour = r'e'

    neutral_vll = r"\nu" in vll

    if boson == r'$H$':
        if neutral_vll:
            return None
        else:
            return r'$\ell$'  # should be tau
    elif boson == r'$Z$':
        # don't allow nu -> Z + nu, otherwise return ell
        if neutral_vll:
            return None
        else:
            return r'$\ell$'
    else:  # W boson
        if neutral_vll:
            return r'$\ell$'
        else:
            return r'$\nu$'

def strip(label):
    label = label.replace('\\', '').replace('$', '').replace('{', '')
    label = label.replace('}', '').replace('*', '').replace('^', '')
    return label.replace(' ', '')

# loop over all options
counter = 0
final_state_lines = []
plotted = []

info_lines = []

for middle_boson_label in sorted(middle_boson_labels):
    for vll_decay_type in sorted(['WW', 'WZ', 'ZZ', 'WH', 'HZ', 'HH']):
        if vll_decay_type in ['WW', 'HH']:
            vll_types = ['LL', 'NL', 'NN']
        elif vll_decay_type in ['ZZ']:
            vll_types = ['LL']
        elif vll_decay_type in ['WZ', 'HZ']:
            vll_types = ['LL', 'NL']
        elif vll_decay_type in ['WH']:
            vll_types = ['LL', 'NL', 'NN', 'LN']

        for vll_type in sorted(['LL', 'NL', 'NN']):
            upper_vll_label = r"$\ell'$" if vll_type[0]=='L' else r"$\nu'$"
            lower_vll_label = r"$\ell'$" if vll_type[1]=='L' else r"$\nu'$"
            same_vll_type = vll_type in ['LL', 'NN']
        
            upper_boson_label = "$"+vll_decay_type[0]+"$"
            lower_boson_label = "$"+vll_decay_type[1]+"$"
            same_boson = upper_boson_label==lower_boson_label
            for up_dp in sorted(boson_decay_products[upper_boson_label]):
                up_dp1, up_dp2 = up_dp
                for dn_dp in sorted(boson_decay_products[lower_boson_label]):
                    dn_dp1, dn_dp2 = dn_dp
                    n_leptons = 0
                    n_jets_upper = 0
                    n_neutrinos_upper = 0
                    n_jets_lower = 0
                    n_neutrinos_lower = 0
                    n_photons_upper = 0
                    n_photons_lower = 0
                    n_gluons_upper = 0
                    n_gluons_lower = 0

                    # each vll can decay into either H W or Z + a lepton
                    # figure out what kind of lepton you'll have
                    upper_decay_lepton = get_corresponding_lepton(upper_vll_label, upper_boson_label)
                    lower_decay_lepton = get_corresponding_lepton(lower_vll_label, lower_boson_label)
                    if upper_decay_lepton is None or lower_decay_lepton is None:
                        continue
                    
                    # count decay leptons
                    if upper_decay_lepton == r'$\ell$':
                        n_leptons += 1
                    else:
                        n_neutrinos_upper += 1
                    if lower_decay_lepton == r'$\ell$':
                        n_leptons += 1
                    else:
                        n_neutrinos_lower += 1

                    # count decay product states
                    for udp in [up_dp1, up_dp2]:
                        if udp == r"$q$":
                            n_jets_upper += 1
                        elif udp == r'$g$':
                            n_gluons_upper += 1
                        elif udp == r'$\ell$':
                            n_leptons += 1
                        elif udp == r'$\nu$':
                            n_neutrinos_upper += 1
                        elif udp == r'$\gamma$':
                            n_photons_upper += 1
                        elif udp == r'$Zqq$':
                            n_jets_upper += 2
                        elif udp == r'$Z\ell\ell$':
                            n_leptons += 2
                        elif udp == r'$Z\nu\nu$':
                            n_neutrinos_upper += 2
                        elif udp == r'$Wqq$':
                            n_jets_upper += 2
                        elif udp == r'$W\ell\nu$':
                            n_leptons += 1
                            n_neutrinos_upper += 1
                    for ldp in [dn_dp1, dn_dp2]:
                        if ldp in r"$q$":
                            n_jets_lower += 1
                        elif ldp == r'$g$':
                            n_gluons_lower += 1
                        elif ldp == r'$\ell$':
                            n_leptons += 1
                        elif ldp == r'$\nu$':
                            n_neutrinos_lower += 1
                        elif ldp == r'$\gamma$':
                            n_photons_lower += 1
                        elif ldp == r'$Zqq$':
                            n_jets_lower += 2
                        elif ldp == r'$Z\ell\ell$':
                            n_leptons += 2
                        elif ldp == r'$Z\nu\nu$':
                            n_neutrinos_lower += 2
                        elif ldp == r'$Wqq$':
                            n_jets_lower += 2
                        elif ldp == r'$W\ell\nu$':
                            n_leptons += 1
                            n_neutrinos_lower += 1

                    # only plot if n_jets <=3
                    # and if n_leptons <=4
                    # we assert no nu -> Z + nu earlier
                    n_jets = n_jets_upper + n_jets_lower
                    n_neutrinos = n_neutrinos_upper + n_neutrinos_lower
                    if n_jets > 4:
                        continue
                    if n_leptons > 4:
                        continue
                    if n_neutrinos > 1:
                        continue

                    # make sure at least one branch is reconstructable
                    lower_reconstructable = (n_neutrinos_lower <= 1) and (n_photons_lower == 0) and (n_gluons_lower == 0)
                    upper_reconstructable = (n_neutrinos_upper <= 1) and (n_photons_upper == 0) and (n_gluons_upper == 0)
                    
                    if not (lower_reconstructable or upper_reconstructable):
                        continue

                    # also check if we've plotted a duplicate:
                    if same_boson and same_vll_type:
                        if [vll_decay_type, vll_type, {up_dp, dn_dp}] in plotted:
                            continue
                        else:
                            plotted.append([vll_decay_type, vll_type, {up_dp, dn_dp}])


                    # initialize figure
                    fig = plt.figure(figsize=(10.,10.))
                    ax = fig.add_axes([0,0,1,1], frameon=False)

                    # initialize diagram
                    diagram = Diagram(ax)

                    # set endpoints (same for all diagrams)
                    in_top = diagram.vertex(xy=(.1,.9), marker='')
                    in_bottom = diagram.vertex(xy=(.1,.1), marker='')
                    left = diagram.vertex(xy=(.3,.5), marker='')
                    right = diagram.vertex(xy=(.55,.5), marker='')
                    upper_vll_vtx = diagram.vertex(xy=(.7,.7), marker='')
                    upper_vll_lep_vtx = diagram.vertex(xy=(.9,.9), marker='')
                    upper_vll_bos_vtx = diagram.vertex(xy=(.8,.65), marker='')
                    upper_bos_dp_up_vtx = diagram.vertex(xy=(.9,.75), marker='')
                    upper_bos_dp_dn_vtx = diagram.vertex(xy=(.9,.55), marker='')
                    lower_vll_vtx = diagram.vertex(xy=(.7,.3), marker='')
                    lower_vll_lep_vtx = diagram.vertex(xy=(.9,.1), marker='')
                    lower_vll_bos_vtx = diagram.vertex(xy=(.8,.35), marker='')
                    lower_bos_dp_up_vtx = diagram.vertex(xy=(.9,.45), marker='')
                    lower_bos_dp_dn_vtx = diagram.vertex(xy=(.9,.25), marker='')

                    # draw incoming quark lines
                    q1 = diagram.line(in_top, left, **fermion_kwargs)
                    q2 = diagram.line(left, in_bottom, **fermion_kwargs)

                    # middle boson
                    mid_bos = diagram.line(left, right, **ew_boson_kwargs)

                    # VLLs and decay products
                    upper_vll = diagram.line(right, upper_vll_vtx, **get_kwargs(upper_vll_label))
                    upper_vll_lep = diagram.line(upper_vll_vtx, upper_vll_lep_vtx, **get_kwargs(upper_decay_lepton))
                    upper_vll_bos = diagram.line(upper_vll_vtx, upper_vll_bos_vtx, **get_kwargs(upper_boson_label))
                    upper_bos_dp_up = diagram.line(upper_vll_bos_vtx, upper_bos_dp_up_vtx, **get_kwargs(up_dp1))
                    upper_bos_dp_dn = diagram.line(upper_bos_dp_dn_vtx, upper_vll_bos_vtx, **get_kwargs(up_dp2))

                    lower_vll = diagram.line(lower_vll_vtx, right, **get_kwargs(lower_vll_label))
                    lower_vll_lep = diagram.line(lower_vll_lep_vtx, lower_vll_vtx, **get_kwargs(lower_decay_lepton))
                    lower_vll_bos = diagram.line(lower_vll_vtx, lower_vll_bos_vtx, **get_kwargs(lower_boson_label))
                    lower_bos_dp_up = diagram.line(lower_vll_bos_vtx, lower_bos_dp_up_vtx, **get_kwargs(dn_dp1))
                    lower_bos_dp_dn = diagram.line(lower_bos_dp_dn_vtx, lower_vll_bos_vtx, **get_kwargs(dn_dp2))

                    # set labels
                    in_top.text(r'$q$', fontsize=30)
                    in_bottom.text(r'$q$', fontsize=30)

                    mid_bos.text(middle_boson_label, fontsize=30, t=0)

                    upper_vll.text(upper_vll_label, fontsize=30, y=0.06)
                    upper_vll_lep.text(upper_decay_lepton, fontsize=30, y=0.06)
                    upper_vll_bos.text(upper_boson_label, fontsize=30, y=-0.06)
                    upper_bos_dp_up.text(up_dp1, fontsize=30, y=0.06)
                    upper_bos_dp_dn.text(up_dp2, fontsize=30, y=0.06)

                    lower_vll.text(lower_vll_label, fontsize=30, y=0.08)
                    lower_vll_lep.text(lower_decay_lepton, fontsize=30, y=0.08)
                    lower_vll_bos.text(lower_boson_label, fontsize=30, y=0.04)
                    lower_bos_dp_up.text(dn_dp1, fontsize=30, y=0.06)
                    lower_bos_dp_dn.text(dn_dp2, fontsize=30, y=0.06)

                    # plot lines on axis
                    diagram.plot()

                    # save figure
                    if upper_vll_label == r"$\ell'$":
                        upper_vll_letter = 'L'
                    else:
                        upper_vll_letter = 'N'
                    
                    if lower_vll_label == r"$\ell'$":
                        lower_vll_letter = 'L'
                    else:
                        lower_vll_letter = 'N'

                    fig_title = strip(f'{upper_boson_label}{lower_boson_label}_{upper_vll_letter}{lower_vll_letter}_{upper_decay_lepton}{lower_decay_lepton}_{up_dp1}{up_dp2}_{dn_dp1}{dn_dp2}.png')
                    plt.savefig(fig_title, dpi=300, transparent=True)
                    plt.cla(); plt.clf()
                    plt.close()
                    info_lines.append(fig_title + " " + str(counter))
                    print(fig_title + " " + str(counter))
                    print(upper_reconstructable, lower_reconstructable)
                    # save info about state
                    info_lines.append(r'| $n_{\ell}$ | $n_{j}$ | $n_{\nu}$ | '+upper_boson_label+r' decay | '+lower_boson_label+r' decay |')

                    info_lines.append(f'| {n_leptons} | {n_jets} | {n_neutrinos} | {up_dp1}{up_dp2} | {dn_dp1}{dn_dp2} |'.replace('$$', ''))

                    counter += 1
                    final_state_line = strip(f"{upper_decay_lepton},{up_dp1},{up_dp2},{lower_decay_lepton},{dn_dp1},{dn_dp2}")
                    final_state_lines.append(final_state_line)

                    plotted.append(vll_decay_type)

with open('final_states.csv', 'w+') as final_state_file:
    final_state_file.write('\n'.join(final_state_lines))

with open('info.txt', 'w+') as info_file:
    info_file.write('\n'.join(info_lines))
