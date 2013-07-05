from unittest import TestCase

import numpy as np
import pandas as pd
import pandas.util.testing as tm

import ts_charting.formatter as formatter
reload(formatter)

plot_index = pd.date_range(start="2000-1-1", freq="D", periods=10000)
class TestTimestampLocator(TestCase):

    def __init__(self, *args, **kwargs):
        TestCase.__init__(self, *args, **kwargs)

    def runTest(self):
        pass

    def setUp(self):
        pass

    def test_inferred_freq(self):
        """
        inferred freqs are based off of min_ticks
        """
        tl = formatter.TimestampLocator(plot_index)
        # showing only the first 10 should give us days
        xticks = tl._process(1, 10)
        assert tl.gen_freq == 'D'

        # showing only the first 70 should give us weeks
        xticks = tl._process(1, 6 * 7 + 1)
        assert tl.gen_freq == 'W'

        # months should trigger at around 6 * 31
        xticks = tl._process(1, 6 * 31 )
        assert tl.gen_freq == 'MS'

        # year should trigger at around 6 *366 
        xticks = tl._process(1, 6 * 366  + 1)
        assert tl.gen_freq == 'AS'

    def test_fixed_freq(self):
        """
        Test passing in a fixed freq. This will allow len(xticks) 
        less than min_ticks
        """
        tl = formatter.TimestampLocator(plot_index, 'MS')
        xticks = tl._process(1, 30*3)
        len(xticks) == 3

        tl = formatter.TimestampLocator(plot_index, 'MS')
        xticks = tl._process(1, 30*6)
        len(xticks) == 6

        tl = formatter.TimestampLocator(plot_index, 'W')
        xticks = tl._process(1, 10*7)
        len(xticks) == 10

        tl = formatter.TimestampLocator(plot_index, 'AS')
        xticks = tl._process(1, 10 * 365)
        len(xticks) == 10

    def test_bool_xticks(self):
        """
        ability to set ticks with a bool series where True == tick
        """
        freq = 'M'
        ds = pd.Series(1, index=plot_index)
        # True when freq market is hit
        bool_ticks = ds.resample(freq).reindex(plot_index).fillna(0).astype(bool)
        tl = formatter.TimestampLocator(plot_index, xticks=bool_ticks)
        xticks = tl._process(0, 90)
        tl = formatter.TimestampLocator(plot_index, freq=freq)
        correct = tl._process(0, 90)
        tm.assert_almost_equal(xticks, correct)

        freq = 'MS'
        ds = pd.Series(1, index=plot_index)
        # True when freq market is hit
        bool_ticks = ds.resample(freq).reindex(plot_index).fillna(0).astype(bool)
        tl = formatter.TimestampLocator(plot_index, xticks=bool_ticks)
        xticks = tl._process(3, 94)
        tl = formatter.TimestampLocator(plot_index, freq=freq)
        correct = tl._process(3, 94)
        tm.assert_almost_equal(xticks, correct)

        freq = 'W'
        ds = pd.Series(1, index=plot_index)
        # True when freq market is hit
        bool_ticks = ds.resample(freq).reindex(plot_index).fillna(0).astype(bool)
        tl = formatter.TimestampLocator(plot_index, xticks=bool_ticks)
        xticks = tl._process(3, 94)
        tl = formatter.TimestampLocator(plot_index, freq=freq)
        correct = tl._process(3, 94)
        tm.assert_almost_equal(xticks, correct)

    def test_list_of_datetimes(self):
        """
        The other xticks option is sending in a DatetimeIndex of the dates you want
        """
        freq = 'M'

        dates = pd.Series(1, index=plot_index).resample(freq).index
        tl = formatter.TimestampLocator(plot_index, xticks=dates)
        test = tl._process(3, 900)

        tl = formatter.TimestampLocator(plot_index, freq=freq)
        correct = tl._process(3, 900)
        tm.assert_almost_equal(test, correct)

        freq = 'MS'
        dates = pd.Series(1, index=plot_index).resample(freq).index
        tl = formatter.TimestampLocator(plot_index, xticks=dates)
        test = tl._process(3, 900)

        tl = formatter.TimestampLocator(plot_index, freq=freq)
        correct = tl._process(3, 900)
        tm.assert_almost_equal(test, correct)

        # straight list of dates
        freq = 'MS'
        dates = pd.Series(1, index=plot_index).resample(freq).index
        dates = list(dates)
        tl = formatter.TimestampLocator(plot_index, xticks=dates)
        test = tl._process(3, 900)

        tl = formatter.TimestampLocator(plot_index, freq=freq)
        correct = tl._process(3, 900)
        tm.assert_almost_equal(test, correct)

if __name__ == '__main__':
    import nose                                                                      
    nose.runmodule(argv=[__file__,'-vs','-x','--pdb', '--pdb-failure'],exit=False)   
