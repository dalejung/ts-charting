from unittest import TestCase

import numpy as np
import pandas as pd
import pandas.util.testing as tm

import ts_charting.figure as figure
reload(figure)
process_series = figure.process_series

class Testprocess_data(TestCase):

    def __init__(self, *args, **kwargs):
        TestCase.__init__(self, *args, **kwargs)

    def runTest(self):
        pass

    def setUp(self):
        pass

    def test_already_aligned(self):
        plot_index = pd.date_range(start="2000", freq="D", periods=100)
        series = pd.Series(range(100), index=plot_index)
        plot_series = process_series(series, plot_index)
        tm.assert_almost_equal(series, plot_series)
        tm.assert_almost_equal(plot_series.index, plot_index)

    def test_partial_plot(self):
        """
        Test plotting series that is a subset of plot_index.
        Should align and fill with nans
        """
        plot_index = pd.date_range(start="2000", freq="D", periods=100)
        series = pd.Series(range(100), index=plot_index)
        series = series[:50] # only first 50
        plot_series = process_series(series, plot_index)

        # have same index
        tm.assert_almost_equal(plot_series.index, plot_index)
        assert plot_series.count() == 50
        assert np.all(plot_series[50:].isnull()) # method=None so fill with nan
        assert np.all(plot_series[:50] == series[:50]) 

    def test_unaligned_indexes(self):
        """
        Test when series.index and plot_index have no common datetimes
        """
        plot_index = pd.date_range(start="2000", freq="D", periods=100)
        series = pd.Series(range(100), index=plot_index)
        # move days to 11 PM the night before
        shift_series = series.tshift(-1, '1h')
        plot_series = process_series(shift_series, plot_index)
        # without method, data doesn't align and we nothing but nans
        tm.assert_almost_equal(plot_series.index, plot_index) # index aligh properly
        assert np.all(plot_series.isnull()) # no data

        # method = 'ffill'
        plot_series = process_series(shift_series, plot_index, method='ffill')
        # without method, data doesn't align and we nothing but nans
        tm.assert_almost_equal(plot_series.index, plot_index) # index align 
        # since we're forward filling a series we tshifted into past
        # plot_series should just equal the original series
        tm.assert_almost_equal(plot_series, series)


    def test_different_freqs(self):
        """
        Tests indexes of differeing frequencies. This is more of repeat
        test of test_partial_plot but with many holes instead of one half missing
        value.
        """
        plot_index = pd.date_range(start="2000-01-01", freq="D", periods=100)
        series = pd.Series(range(100), index=plot_index)
        grouped_series = series.resample('MS', 'max')
        plot_series = process_series(grouped_series, plot_index)
        tm.assert_almost_equal(plot_series.index, plot_index) # index align 
        # method=None, dropna should give back same series
        tm.assert_almost_equal(plot_series.dropna(), grouped_series)

        plot_series = process_series(grouped_series, plot_index, method='ffill')
        tm.assert_almost_equal(plot_series.index, plot_index) # index align 
        assert plot_series.isnull().sum() == 0
        month_ind = plot_series.index.month - 1
        # assert that each value corresponds to its month in grouped_series
        assert np.all(grouped_series[month_ind] == plot_series)

    def test_scalar(self):
        """
        Test the various ways we handle scalars. 
        """
        plot_index = pd.date_range(start="2000-01-01", freq="D", periods=100)
        plot_series = process_series(5, plot_index)
        tm.assert_almost_equal(plot_series.index, plot_index) # index align 
        assert np.all(plot_series == 5)

        # explicitly pass in the series index. Should have a plot_series with only iloc[10:20] 
        # equal to the scalar 5.
        plot_series = process_series(5, plot_index, series_index=plot_index[10:20])
        tm.assert_almost_equal(plot_series.index, plot_index) # index align 
        assert np.all(plot_series[10:20] == 5)
        assert plot_series.isnull().sum() == 90

        # no plot_index. This still works because we're passing in series_index
        plot_series = process_series(5, None, series_index=plot_index[10:20])
        correct = pd.Series(5, index=plot_index[10:20])
        tm.assert_almost_equal(correct, plot_series)

        # without any index, a scalar will error. Cannot plot a scalar on an 
        # empty plot without passing in an index
        try:
            plot_series = process_series(5, None)
        except:
            pass
        else:
            assert False, "scalar should fail without plot_index or series_index"

    def test_iterable(self):
        """
        Non pd.Series iterables require an equal length series_index or 
        plot_index.
        """
        try:
            plot_series = process_series(range(10), None)
        except:
            pass
        else:
            assert False, "iterable should fail without plot_index or series_index"

        plot_index = pd.date_range(start="2000-01-01", freq="D", periods=100)
        try:
            plot_series = process_series(range(10), plot_index)
        except:
            pass
        else:
            assert False, "iterable requires an index of same length"

        # equal length, good times
        plot_series = process_series(range(10), plot_index[:10])
        correct = pd.Series(range(10), index=plot_index[:10])
        tm.assert_almost_equal(correct, plot_series)

if __name__ == '__main__':
    import nose                                                                      
    nose.runmodule(argv=[__file__,'-vvs','-x','--pdb', '--pdb-failure'],exit=False)   
