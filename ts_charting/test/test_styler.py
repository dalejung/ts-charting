from unittest import TestCase
import pandas as pd
import numpy as np

import ts_charting.styles as styles
level_styler = styles.level_styler


class TestStyler(TestCase):
    # testing base pandas

    def __init__(self, *args, **kwargs):
        TestCase.__init__(self, *args, **kwargs)

    def runTest(self):
        pass

    def setUp(self):
        pass

    def test_level_styler(self):
        """
        Test level styler. 
        """
        df = pd.DataFrame({'value':np.random.randn(100)})
        df['num_cat'] = np.random.choice(list(range(5)), 100) * 100
        df['name'] = np.random.choice(['dale', 'bob', 'wes', 'frank'], 100)

        styles = level_styler(color=df.num_cat, linestyle=df.name)
        style_df = pd.DataFrame(styles)

        for name in df.name.unique():
            inds = df.name == name
            # all values with the same name shoudl have same linestyle
            assert len(np.unique(style_df.ix[inds].linestyle)) == 1

        for i in df.num_cat.unique():
            inds = df.num_cat == i
            # all values with the same name shoudl have same color
            assert len(np.unique(style_df.ix[inds].color)) == 1

if __name__ == '__main__':                                                                                          
    import nose                                                                      
    nose.runmodule(argv=[__file__,'-vvs','-x','--pdb', '--pdb-failure'],exit=False)   
