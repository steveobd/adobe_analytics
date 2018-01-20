import datetime

import unittest
import adobe_analytics


class UtilsTest(unittest.TestCase):
    def setUp(self):
        fake_list = [{"id":"123", "title":"abc"},{"id":"456","title":"abc"}]

        self.alist = adobe_analytics.Value.list("segemnts", fake_list, {})

    def tearDown(self):
        del self.alist

    def test_addressable_list_repr_html_(self):
        """Test the _repr_html_ for AddressableList this is used in ipython """
        outlist = '<table><tr><td><b>ID</b></td><td><b>Title</b></td></tr><tr><td><b>123</b></td><td>abc</td></tr><tr><td><b>456</b></td><td>abc</td></tr></table>'
        self.assertEqual(self.alist._repr_html_(),outlist,\
                         "The _repr_html_ isn't working: {}"\
                         .format(self.alist._repr_html_()))

    def test_addressable_list_str_(self):
        """Test _str_ method """
        outstring = 'ID 123                       | Name: abc \nID 456                       | Name: abc \n'
        self.assertEqual(self.alist.__str__(), outstring,
                         "The __str__ isn't working: {}"
                         .format(self.alist.__str__()))

    def test_addressable_list_get_time(self):
        """ Test the custom get item raises a problem when there are duplicate names """
        with self.assertRaises(KeyError):
             self.alist['abc']
             
    def test_wrap(self):
        """Test the wrap method """
        self.assertIsInstance(adobe_analytics.utils.wrap("test"), list)
        self.assertIsInstance(adobe_analytics.utils.wrap(["test"]), list)
        self.assertEqual(adobe_analytics.utils.wrap("test"), ["test"])
        self.assertEqual(adobe_analytics.utils.wrap(["test"]), ["test"])

    def test_date(self):
        """Test the Date Method"""
        test_date = "2016-09-01"
        self.assertEqual(adobe_analytics.utils.date(None), None)
        self.assertEqual(adobe_analytics.utils.date(test_date).strftime("%Y-%m-%d"),
                         test_date)
        d = datetime.date(2016, 9, 1)
        self.assertEqual(adobe_analytics.utils.date(d).strftime("%Y-%m-%d"),
                         test_date)
    
        t = datetime.datetime(2016, 9, 1)
        self.assertEqual(adobe_analytics.utils.date(t).strftime("%Y-%m-%d"),
                         test_date)
        
        self.assertEqual(adobe_analytics.utils.date(u"2016-09-01").strftime("%Y-%m-%d"),
                         test_date)
        with self.assertRaises(ValueError):
            adobe_analytics.utils.date({})
            
    def test_affix(self):
        """Test the Affix method to make sure it handles things correctly"""
        p = "pre"
        s = "suf"
        v = "val"
        con = "+"
        
        self.assertEqual(adobe_analytics.utils.affix(v, p, connector=con),
                         con.join([p, v]))
        self.assertEqual(adobe_analytics.utils.affix(base=v, suffix=s, connector=con),
                         con.join([v, s]))
        self.assertEqual(adobe_analytics.utils.affix(v, p, s, connector=con),
                         con.join([p, v, s]))
        self.assertEqual(adobe_analytics.utils.affix(base=v, connector=con),
                         con.join([v]))
    
    def test_translate(self):
        """Test the translate method """
        t = {"product": "cat_collar", "price": 100, "location": "no where"}
        m = {"product": "Product_Name","price": "Cost","date": "Date"}
        s = {"Product_Name": "cat_collar", "Cost": 100, "location": "no where"}
        self.assertEqual(adobe_analytics.utils.translate(t, m), s)
