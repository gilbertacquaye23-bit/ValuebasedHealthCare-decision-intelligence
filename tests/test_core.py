"""Exercise policy optimization definitions without CMS downloads or tuning."""
import ast
import json
from pathlib import Path
import numpy as np
import pandas as pd

NOTEBOOK = Path(__file__).resolve().parents[1] / 'notebooks/healthcare_policy_optimization.ipynb'

def namespace():
    notebook = json.loads(NOTEBOOK.read_text())
    ns = {'np': np, 'pd': pd, 'STATE_DIMS': (3,)*4, 'N_STATES':81, 'N_ACTIONS':6}
    # Constant definitions and functions/classes are tested directly from source.
    for cell in notebook['cells']:
        if cell['cell_type'] != 'code':
            continue
        tree = ast.parse(''.join(cell['source']))
        nodes = [node for node in tree.body if isinstance(node,(ast.FunctionDef,ast.ClassDef)) or isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id in {'ACTIONS','ACTION_NAMES'} for t in node.targets)]
        exec(compile(ast.Module(body=nodes,type_ignores=[]),str(NOTEBOOK),'exec'),ns)
    return ns

def test_allocations_and_state_index():
    ns = namespace()
    assert np.allclose(ns['ACTIONS'].sum(axis=1),1)
    assert (ns['ACTIONS'] >= 0).all()
    assert ns['state_to_index']((2,2,2,2)) == 80

def test_terminal_update_and_zero_planning():
    agent = namespace()['DynaQAgent'](alpha=.05,planning_steps=0)
    agent.q[1,:] = 100
    agent.update(0,0,2,1,True)
    assert np.isclose(agent.q[0,0],.1)
    assert agent.plan() == []

def test_environment_training_and_baseline_discount():
    ns = namespace()
    data = pd.DataFrame({'facility_id':['000001','000002','000003'], 'mspb_score':[.8,1,1.2], 'excess_readmission_ratio':[.9,1,1.1], 'hvbp_efficiency_score':[.5,1,1.5], 'discharges':[100,200,300]})
    for name,col in [('MSPB_CUTS','mspb_score'),('READMIT_CUTS','excess_readmission_ratio'),('HVBP_CUTS','hvbp_efficiency_score'),('DISCHARGE_CUTS','discharges')]:
        ns[name] = ns['tertile_cutpoints'](data[col])
    env = ns['CMSCalibratedVBHCEnv'](data)
    env.reset(seed=7)
    for i in range(12):
        state,reward,done,_ = env.step(0)
        assert np.isfinite(reward) and -1 <= reward <= 1
        assert done == (i == 11)
    a,t,_ = ns['train_dynaq'](data,episodes=5,planning_steps=1,seed=8)
    b,u,_ = ns['train_dynaq'](data,episodes=5,planning_steps=1,seed=8)
    assert np.array_equal(a.q,b.q)
    assert len(t) == 5
    # At gamma=1, discounted return must equal undiscounted episode reward.
    baseline = ns['evaluate_equal_baseline'](data,episodes=3,seed=9,gamma=1)
    assert np.allclose(baseline.episode_reward,baseline.discounted_return)


def test_fraction_scores_and_hospital_merge():
    """Exercise the actual preparation cells with CMS-style reported values."""
    import re
    ns = namespace()
    ns.update(re=re, display=lambda *args: None)
    scores = ns['numeric'](pd.Series(['1 out of 10', '0 out of 10', '3 out of 10', 'Not Available', '1 out of 0', '0.99']))
    assert np.allclose(scores.iloc[:3], [.1, 0, .3])
    assert scores.iloc[3:5].isna().all()
    assert scores.iloc[5] == .99
    ns['hrrp_raw'] = pd.DataFrame({'facility_id':['010001','010005'], 'excess_readmission_ratio':['0.98','1.02'], 'number_of_discharges':['100','200']})
    ns['mspb_raw'] = pd.DataFrame({'facility_id':['010001','010005'], 'score':['0.99','1.01']})
    ns['hvbp_raw'] = pd.DataFrame({'facility_id':['010001','010005'], 'mspb1_measure_score':['1 out of 10','3 out of 10']})
    notebook = json.loads(NOTEBOOK.read_text())
    for i in (10,12):
        exec(''.join(notebook['cells'][i]['source']),ns)
    assert len(ns['real_hospitals']) == 2
    assert np.allclose(ns['real_hospitals'].hvbp_efficiency_score,[.1,.3])
    ns['hvbp_raw']['mspb1_measure_score'] = 'Not Available'
    try:
        exec(''.join(notebook['cells'][10]['source']),ns)
    except ValueError as exc:
        assert 'HVBP has no usable' in str(exc)
    else:
        raise AssertionError('Empty HVBP input must stop before training')


def test_pagination_handles_server_page_cap():
    import re
    from types import SimpleNamespace
    offsets = []
    def get(url, params, timeout):
        offset = params['offset']
        offsets.append(offset)
        data = [{'facility_id': str(offset)}] if offset < 2 else []
        return SimpleNamespace(raise_for_status=lambda: None, json=lambda: {'results':data})
    ns = namespace()
    ns.update(re=re, requests=SimpleNamespace(get=get))
    table = ns['fetch_cms_provider_dataset']('example',page_size=5000)
    assert len(table) == 2
    assert offsets == [0,1,2]
