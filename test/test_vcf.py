from yltk.vcf import VcfParser, VcfWriter
from .setup import TestCase


class TestVcfParser(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_header(self):
        parser = VcfParser(f'{self.indir}/tiny.vcf.gz')
        expected = f'''\
##fileformat=VCFv4.3
##fileDate=20090805
##source=myImputationProgramV3.1
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tNA00001\tNA00002\tNA00003'''
        self.assertEqual(expected, parser.header)
        parser.close()

    def test_columns(self):
        parser = VcfParser(f'{self.indir}/tiny.vcf.gz')
        expected = [
            'CHROM',
            'POS',
            'ID',
            'REF',
            'ALT',
            'QUAL',
            'FILTER',
            'INFO',
            'FORMAT',
            'NA00001',
            'NA00002',
            'NA00003',
        ]
        self.assertListEqual(expected, parser.columns)
        parser.close()

    def test_next(self):
        parser = VcfParser(vcf=f'{self.indir}/tiny.vcf.gz')

        first_variant = parser.next()
        expected = {
            'CHROM': '1',
            'POS': '101',
            'ID': 'rs6054257',
            'REF': 'G',
            'ALT': 'A',
            'QUAL': '29',
            'FILTER': 'PASS',
            'INFO': 'NS=3;DP=14;AF=0.5;DB;H2',
            'FORMAT': 'GT:GQ:DP:HQ',
            'NA00001': '0|0:48:1:51,51',
            'NA00002': '1|0:48:8:51,51',
            'NA00003': '1/1:43:5:.,.',
        }
        self.assertDictEqual(expected, first_variant)

        second_variant = parser.next()
        expected = {
            'CHROM': '2',
            'POS': '102',
            'ID': '.',
            'REF': 'T',
            'ALT': 'A',
            'QUAL': '3',
            'FILTER': 'q10',
            'INFO': 'NS=3;DP=11;AF=0.017',
            'FORMAT': 'GT:GQ:DP:HQ',
            'NA00001': '0|0:49:3:58,50',
            'NA00002': '0|1:3:5:65,3',
            'NA00003': '0/0:41:3:.',
        }
        self.assertDictEqual(expected, second_variant)

        third_variant = parser.next()
        expected = {
            'CHROM': '3',
            'POS': '103',
            'ID': 'rs6040355',
            'REF': 'A',
            'ALT': 'G,T',
            'QUAL': '67',
            'FILTER': 'PASS',
            'INFO': 'NS=2;DP=10;AF=0.333,0.667;AA=T;DB',
            'FORMAT': 'GT:GQ:DP:HQ',
            'NA00001': '1|2:21:6:23,27',
            'NA00002': '2|1:2:0:18,2',
            'NA00003': '2/2:35:4:.',
        }
        self.assertDictEqual(expected, third_variant)

        end_of_file = parser.next()
        self.assertEqual(None, end_of_file)

        parser.close()

    def test_context_iterator(self):
        with VcfParser(vcf=f'{self.indir}/tiny.vcf.gz') as parser:
            actual = [variant for variant in parser]

        expected = [
            {
                'CHROM': '1',
                'POS': '101',
                'ID': 'rs6054257',
                'REF': 'G',
                'ALT': 'A',
                'QUAL': '29',
                'FILTER': 'PASS',
                'INFO': 'NS=3;DP=14;AF=0.5;DB;H2',
                'FORMAT': 'GT:GQ:DP:HQ',
                'NA00001': '0|0:48:1:51,51',
                'NA00002': '1|0:48:8:51,51',
                'NA00003': '1/1:43:5:.,.',
            },
            {
                'CHROM': '2',
                'POS': '102',
                'ID': '.',
                'REF': 'T',
                'ALT': 'A',
                'QUAL': '3',
                'FILTER': 'q10',
                'INFO': 'NS=3;DP=11;AF=0.017',
                'FORMAT': 'GT:GQ:DP:HQ',
                'NA00001': '0|0:49:3:58,50',
                'NA00002': '0|1:3:5:65,3',
                'NA00003': '0/0:41:3:.',
            },
            {
                'CHROM': '3',
                'POS': '103',
                'ID': 'rs6040355',
                'REF': 'A',
                'ALT': 'G,T',
                'QUAL': '67',
                'FILTER': 'PASS',
                'INFO': 'NS=2;DP=10;AF=0.333,0.667;AA=T;DB',
                'FORMAT': 'GT:GQ:DP:HQ',
                'NA00001': '1|2:21:6:23,27',
                'NA00002': '2|1:2:0:18,2',
                'NA00003': '2/2:35:4:.',
            }
        ]

        self.assertListEqual(expected, actual)


class TestVcfWriter(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_wrong_header_1(self):
        writer = VcfWriter(vcf=f'{self.outdir}/write.vcf')

        # does not start with '##'
        header = f'''\
fileformat=VCFv4.3
##fileDate=20090805'''
        with self.assertRaises(AssertionError):
            writer.write_header(header)

        writer.close()

    def test_wrong_header_2(self):
        writer = VcfWriter(vcf=f'{self.outdir}/write.vcf')

        # no column names
        header = f'''\
##fileformat=VCFv4.3
##fileDate=20090805'''

        with self.assertRaises(AssertionError):
            writer.write_header(header)

        writer.close()

    def test_cannot_write_header_twice(self):
        writer = VcfWriter(vcf=f'{self.outdir}/write.vcf')

        header = f'''\
##fileformat=VCFv4.3
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tNA00001\tNA00002\tNA00003'''

        writer.write_header(header)  # write 1st time

        with self.assertRaises(AssertionError):
            writer.write_header(header)  # write 2nd time

        writer.close()

    def test_write_variant(self):
        writer = VcfWriter(vcf=f'{self.outdir}/write.vcf')

        header = f'''\
##fileformat=VCFv4.3
##fileDate=20090805
##source=myImputationProgramV3.1
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tNA00001\tNA00002\tNA00003'''

        writer.write_header(header)

        variant = {
            'CHROM': 1,
            'POS': 101,
            'ID': 'rs6054257',
            'REF': 'G',
            'ALT': 'A',
            'QUAL': 29,
            'FILTER': 'PASS',
            'INFO': 'NS=3;DP=14;AF=0.5;DB;H2',
            'FORMAT': 'GT:GQ:DP:HQ',
            'NA00001': '0|0:48:1:51,51',
            'NA00002': '1|0:48:8:51,51',
            'NA00003': '1/1:43:5:.,.',
        }

        writer.write(variant)

        writer.close()
