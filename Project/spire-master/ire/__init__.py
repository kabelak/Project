#!/usr/bin/env python
# Copyright (C) 2008-2012 Kai Blin <kai.blin@biotech.uni-tuebingen.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys
import re
import subprocess
import logging
from Bio.Blast import NCBIXML

FORWARD_PATTERN = '(C|A).....(CAGUG|CAAUG|GAGAG|UAGUA|CAGCG|CUGUG)'
REVERSE_PATTERN = '(CACAG|CACUG|CAUUG|CUCUC|UACUA|CGCUG).....(G|U)'
FORWARD = 1
REVERSE = -1
UTR_LEN = 200
MAX_ALN_RESULTS = 6
E_VAL_THRESH = 0.04


class CDS:
    """coding sequence datatype"""

    def __init__(self, feature, seq_str):
        """create CDS"""
        self.qualifiers = feature.qualifiers
        self.location = feature.location
        self.strand = feature.strand
        self.mrna = seq_str[feature.location.nofuzzy_start - UTR_LEN: \
            feature.location.nofuzzy_end + UTR_LEN]
        if self.strand == REVERSE:
            self.mrna = self.mrna.reverse_complement()

    def start(self):
        """get the start of the CDS"""
        return self.location.nofuzzy_start

    def end(self):
        """get the end of the CDS"""
        return self.location.nofuzzy_end


class FeatureMatch:
    """The main datatype of SPIRE"""

    def __init__(self, feature, dist, position=""):
        """Create a FeatureMatch"""
        self.feature = feature
        self.dist = dist
        self.position = position
        self.qualifiers = feature.qualifiers
        self.n_align = []
        self.p_align = []

    def start(self):
        """Start of the FeatureMatch"""
        return self.feature.start()

    def end(self):
        """End of the FeatureMatch"""
        return self.feature.end()

    def __str__(self):
        if self.qualifiers.has_key('locus_tag'):
            return self.qualifiers['locus_tag'][0]
        elif self.qualifiers.has_key('gene'):
            return self.qualifiers['gene'][0]
        else:
            return self.qualifiers['note'][0]

    def feature_fasta(self, loop=None):
        """Print a FASTA version of the feature's RNA sequence"""
        ret = ""
        ret = ">"
        ret += "%s" % self.__str__()
        if self.qualifiers.has_key('protein_id'):
            ret += "|%s" % self.qualifiers['protein_id'][0]
        else:
            ret += "None"
        ret += "|%s:%s|" % (self.start(), self.end())
        if self.qualifiers.has_key('product'):
            ret += "%s %s %s" % (self.dist, self.position,
                                 self.qualifiers['product'][0])
        else:
            ret += "not near any known protein"
        if loop is not None:
            ret += "|%s" % loop
        ret += "\n"
        ret += "%s" % self.feature.mrna
        ret += "\n"
        return ret

    def protein_fasta(self, loop=None):
        """Print a FASTA version of the feature's protein sequence"""
        if not self.qualifiers.has_key('translation'):
            print >> sys.stderr, "no translation for %s" % self.__str__()
            return ""
        ret = ""
        ret = ">"
        ret += "%s" % self.__str__()
        if self.qualifiers.has_key('protein_id'):
            ret += "|%s" % self.qualifiers['protein_id'][0]
        else:
            ret += "None"
        ret += "|%s:%s|" % (self.start(), self.end())
        if self.qualifiers.has_key('product'):
            ret += "%s %s %s" % (self.dist, self.position,
                                 self.qualifiers['product'][0])
        else:
            ret += "not near any known protein"
        if loop is not None:
            ret += "|%s" % loop
        ret += "\n"
        ret += "%s" % self.qualifiers['translation'][0]
        ret += "\n"
        return ret


def get_best_hsp(alignment):
    """Return the best HSP of an alignment"""
    max_score = 0
    best_hsp = None
    for hsp in alignment.hsps:
        if hsp.score > max_score:
            max_score = hsp.score
            best_hsp = hsp

    return best_hsp


def is_same_position(feature_match, alignment):
    """Check if a feature is up- or downstream in the alignments as well"""
    # a simple match on the feature's position doesn't work, as that'll
    # break the full genome blast.
    if feature_match.position == "upstream of":
        position = "downstream"
    elif feature_match.position == "downstream of":
        position = "upstream"
    else:
        # no position? better pretend it's the same position
        return True
    pattern = re.compile(position)
    match = pattern.search(alignment.title)
    if match is None:
        return True
    return False


def is_same_gene(feature_match, alignment):
    """Check if the locus tag of the feature is the same as the one from the alignment"""
    pattern = re.compile(feature_match.__str__())
    match = pattern.search(alignment.title)
    if match is None:
        return False
    return True


def is_same_loop_sequence(loop_seq, alignment):
    """Check if the loop sequence of the feature is the same as in the alignment"""
    fields = alignment.title.split("|")
    if len(fields) < 7:
        # No loop sequence in blast annotation, pretend loop sequence is the same
        return True
    print >> sys.stderr, "Comparing %r with %r: " % (loop_seq, fields[6]),
    if unicode(loop_seq) == fields[6]:
        print >> sys.stderr, "match"
        return True
    print >> sys.stderr, "mismatch"
    return False


class Match(object):
    """datatype for an IRE match"""

    def __init__(self, re_match, sequence, direction):
        """initialize IRE match"""
        self.re_match = re_match
        if direction == REVERSE:
            self.sequence = sequence.reverse_complement()
        else:
            self.sequence = sequence
        self.fold_graph = None
        self.two_d_fold_graph = None
        self.direction = direction
        self.features = []
        self.position = 0
        self.before_start = 6
        self.loop_start = 11
        self.loop_length = 5

    def start(self):
        """start of the match"""
        return self.re_match.span()[0]

    def end(self):
        """end of the match"""
        return self.re_match.span()[1]

    def get_loop(self):
        """get the loop match"""
        start = self.loop_start
        end = start + 5
        return self.sequence[start:end]

    def get_before(self):
        """get stem before the loop match"""
        start = self.before_start
        end = start + 5
        return self.sequence[start:end]

    def get_after(self):
        """get stem after the loop match"""
        start = self.loop_start + self.loop_length
        end = start + 6
        return self.sequence[start:end]

    def __str__(self):
        ret = "Match at (%s:%s)" % (self.start(), self.end())
        ret += "\n\tDirection: "
        if self.direction == FORWARD:
            ret += "forward"
        else:
            ret += "reverse"
        ret += "\n\tLoop region: %s" % self.get_loop()
        ret += "\n\tSequence: %s" % self.sequence
        if self.fold_graph is not None:
            padding = " " * (self.loop_start - self.before_start)
            ret += "\n\tFolds to: %s%s" % (padding, self.fold_graph)
        for feature in self.features:
            ret += "\n\tFeature: %s " % feature.position
            product = "unknown product"
            if feature.qualifiers.has_key('product'):
                product = feature.qualifiers["product"][0]
            protein_id = "no id"
            if feature.qualifiers.has_key('protein_id'):
                protein_id = feature.qualifiers["protein_id"][0]
            ret += "%s (%s)" % (product, protein_id)
            ret += "\n\tDistance: %s" % feature.dist
            ret += "\n\tPosition: %s..%s" % (feature.start() + 1, feature.end())
            if feature.qualifiers.has_key('locus_tag'):
                ret += "\n\tURL: http://www.ncbi.nlm.nih.gov/sites/entrez?"
                ret += "db=gene&cmd=search&term="
                ret += feature.qualifiers["locus_tag"][0]
            ret += "\n\tAlignments: %s protein-based, %s rna-based" % \
                   (len(feature.p_align), len(feature.n_align))
            count = 0
            for align in feature.p_align:
                # if not is_same_position(feature, align):
                #    #ret += "\n\t\t[hit not in the same UTR]"
                #    continue
                if is_same_gene(feature, align):
                    continue
                if not count < MAX_ALN_RESULTS:
                    ret += "\n\t\t..."
                    break
                ret += "\n\t\tp-a: %s" % align.title
                length = len(feature.qualifiers['translation'][0])
                hsp = get_best_hsp(align)
                len_pc = (hsp.align_length / float(length) * 100)
                id_pc = (hsp.identities / float(length) * 100)
                ret += " (%0.2f%%, id: %0.2f%%, gaps: %s)" % (len_pc, id_pc,
                                                              hsp.gaps)
                count += 1
            count = 0
            for align in feature.n_align:
                # if not is_same_position(feature, align):
                #    #ret += "\n\t\t[hit not in the same UTR]"
                #    continue
                if is_same_gene(feature, align):
                    continue
                if not count < MAX_ALN_RESULTS:
                    ret += "\n\t\t..."
                    break
                ret += "\n\t\tn-a: %s" % align.title
                length = feature.end() - feature.start()
                hsp = get_best_hsp(align)
                len_pc = (hsp.align_length / float(length) * 100)
                id_pc = (hsp.identities / float(length) * 100)
                ret += " (%0.2f%%, id: %0.2f%%, gaps: %s)" % (len_pc, id_pc,
                                                              hsp.gaps)
                count += 1
        return ret

    def fasta(self):
        """create FASTA output for match"""
        ret = ">%s:%s" % (self.start(), self.end())
        for feature in self.features:
            if feature.qualifiers.has_key('protein_id'):
                ret += "|%s" % feature.qualifiers['protein_id'][0]
            else:
                ret += "|None"
            if feature.qualifiers.has_key('product'):
                ret += "%s %s" % (self.position,
                                  feature.qualifiers['product'][0])
            else:
                ret += "not near any known protein"
        ret += "\n"
        ret += self.sequence
        return ret

    def feature_fasta(self):
        """create nucleotide FASTA output for all features"""
        ret = ""
        for feature in self.features:
            ret += feature.feature_fasta(self.get_loop())
        return ret

    def protein_fasta(self):
        """create protein FASTA output for all features"""
        ret = ""
        for feature in self.features:
            ret += feature.protein_fasta(self.get_loop())
        return ret


def find_matches(sequence, search_pattern, direction):
    """find IRE regex matches on a sequence"""
    match_list = []
    itr = search_pattern.finditer(str(sequence))
    for i in itr:
        offset_d = 5
        offset_u = 10
        if direction == REVERSE:
            offset_d = 10
            offset_u = 5

        match_list.append(Match(i,
                                sequence[i.span()[0] - offset_d: \
                                    i.span()[1] + offset_u],
                                direction))

    return match_list


def find_cds_features(seq_item, sequence):
    """find CDS feature annotations"""
    cds_list = []
    for feature in seq_item.features:
        if feature.type == "CDS":
            cds_list.append(CDS(feature, sequence))
    return cds_list


def set_position(match, feature, direction, hits_within_genes):
    """create FeatureMatch instance for a match close to a feature"""
    if match.end() < feature.start() and \
                            feature.start() - match.end() < UTR_LEN:
        f_match = FeatureMatch(feature, feature.start() - match.end())
        if direction == FORWARD:
            f_match.position = "upstream of"
        else:
            f_match.position = "downstream of"
        match.features.append(f_match)
    elif match.start() > feature.end() and \
                            match.start() - feature.end() < UTR_LEN:
        f_match = FeatureMatch(feature, match.start() - feature.end())
        if direction == FORWARD:
            f_match.position = "downstream of"
        else:
            f_match.position = "upstream of"
        match.features.append(f_match)
    elif hits_within_genes and ( match.start() > feature.start() and
                                         match.end() < feature.end()):
        match.features.append(FeatureMatch(feature, 0, "within"))
        return
    else:
        return


def find_close_features(match, cds_list):
    """get a list of features close to the match"""
    len_cds_list = len(cds_list)
    left = 0
    right = len_cds_list
    while left < right:
        i = (left + right) / 2
        feature = cds_list[i]
        if feature.end() > match.start():
            right = i
        elif match.start() - feature.end() > UTR_LEN:
            left = i + 1
        else:
            break
    start = i > 5 and i - 5 or 0

    return cds_list[start:i + 5]


def annotate_with_cds(match_list, cds_list, hits_within_genes=False):
    """Annotate features with nearby CDS"""
    for match in match_list:
        close_features = find_close_features(match, cds_list)
        for feature in close_features:
            # do a binary search for close features
            if match.direction != feature.strand:
                continue
            set_position(match, feature, feature.strand, hits_within_genes)


def can_pair(base_a, base_b):
    """Check if two RNA bases can pair"""
    first = base_a.lower()
    second = base_b.lower()
    if first == 'a':
        return second == 'u'
    if first == 'c':
        return second == 'g'
    if first == 'g':
        if second in ('c', 'u'):
            return True
        return False
    if first == 'u':
        if second in ('a', 'g'):
            return True
        return False


def filter_fold(match_list):
    """Filter regex matches so only stem loops remain"""
    stem_loops = []
    for match in match_list:
        # pylint: disable-msg=W0511
        # Now comes the tricky part, a seq looks like this:
        # XXXXXCNNNNNCAGUGMMMMMXXXXX
        # Now, the NNNNN before the loop should pair to MMMMM after the loop.
        # Unfortunately, U=G pairs can happen as well, so simply
        # checking if the reverse complement of NNNNN is equal to MMMMM
        # does not work. Also, we might have one more base than just
        # CAGUG in the loop, as in hferritin.
        # We need to check base by base, taking the extra base into
        # account
        stem_before = match.get_before()
        stem_after = match.get_after()
        graph_before = ""
        graph_after = ""
        graph_loop = "....."
        six_base_loop = False

        does_pair = False
        mismatches = 0
        # offset to skip non-pairing first base
        offset = 0
        i = 0
        while (i < 5):
            i_b = (-1 * i) - 1
            i_a = i + offset

            try:
                does_pair = can_pair(stem_before[i_b], stem_after[i_a])
            except IndexError:
                does_pair = False
            # We allow one mismatch total
            if not does_pair:
                mismatches += 1
                graph_after += "."
                graph_before = "." + graph_before
            else:
                graph_after += ")"
                graph_before = "(" + graph_before
            # We allow a mismatch at the first base after the loop
            if offset == 0 and mismatches > 1:
                offset = 1
                i = 0
                mismatches = 0
                graph_loop += "."
                graph_before = ""
                graph_after = ""
                six_base_loop = True
                continue

            i += 1
            if mismatches > 1:
                break
        if mismatches < 2:
            match.fold_graph = "." + graph_before + graph_loop + graph_after
            match.six_base_loop = six_base_loop
            stem_loops.append(match)

    return stem_loops


def run_blastn(match, blastdb):
    """run blastn"""
    from Bio.Blast.Applications import NcbiblastnCommandline

    for feature in match.features:
        rec = None
        try:
            cline = NcbiblastnCommandline(db=blastdb, outfmt=5, num_threads=4)
            pipe = subprocess.Popen(str(cline), shell=True,
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            pipe.stdin.write(feature.feature_fasta())
            pipe.stdin.close()
            recs = NCBIXML.parse(pipe.stdout)
            rec = recs.next()
            pipe.stdout.close()
            pipe.stderr.close()
        except OSError, err:
            logging.warning("Failed to run blastn: %s" % err)
            continue
        except ValueError, err:
            logging.warning("Parsing blast output failed: %s" % err)
            continue
        if not rec:
            continue
        for aln in rec.alignments:
            for hsp in aln.hsps:
                if hsp.expect < E_VAL_THRESH:
                    feature.n_align.append(aln)
                    break


def run_blastp(match, blastdb):
    """run blastp"""
    from Bio.Blast.Applications import NcbiblastpCommandline

    for feature in match.features:
        rec = None
        fasta = feature.protein_fasta()
        if fasta == "":
            continue
        try:
            cline = NcbiblastpCommandline(db=blastdb, outfmt=5, num_threads=4)
            pipe = subprocess.Popen(str(cline), shell=True,
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            pipe.stdin.write(fasta)
            pipe.stdin.close()
            recs = NCBIXML.parse(pipe.stdout)
            rec = recs.next()
            pipe.stdout.close()
            pipe.stderr.close()
        except OSError, err:
            logging.warning("Failed to run blastp: %s" % err)
            continue
        except ValueError, err:
            logging.warning("Parsing blast output failed: %s" % err)
            continue
        if not rec:
            continue
        for aln in rec.alignments:
            for hsp in aln.hsps:
                if hsp.expect < E_VAL_THRESH:
                    feature.p_align.append(aln)
                    break


def blast(match_list, blastdb):
    """run blast searches"""
    import os.path

    blastn = run_blastn
    blastp = run_blastp
    if not os.path.isfile("%s.nin" % blastdb):
        logging.warning("blastn database not found, skipping blastn")
        blastn = lambda x, y: None
    if not os.path.isfile("%s.pin" % blastdb):
        logging.warning("blastp database not found, skipping blastp")
        blastp = lambda x, y: None

    for match in match_list:
        blastn(match, blastdb)
        blastp(match, blastdb)


def filter_align(match_list):
    """filter out matches that don't have an alignment to other genomes"""
    matches = []
    for match in match_list:
        appended = False
        for feature in match.features:
            if feature.n_align != [] or feature.p_align != []:
                if not appended:
                    matches.append(match)
                    appended = True
            else:
                match.features.remove(feature)

    return matches


def filter_utr(match_list):
    """Filter out matches not in the 5' or 3' UTR"""
    """algorithm picks up the matches (ie, "Match at (....:....)" entries in SPIRE output,
    looks at whether the "Feature" field is populated (with eg: down/upstream of bla bla bla),
    and if it is, returns the match as an UTR"""
    filtered_matches = []
    for match in match_list:
        if match.features != []:
            filtered_matches.append(match)
    return filtered_matches


def filter_real_protein(match_list):
    """filter out hypothetical proteins"""
    pat = re.compile("hypothetical protein")
    matches = []
    for match in match_list:
        remove_list = []
        for feat in match.features:
            if not feat.qualifiers.has_key('product'):
                continue
            product = feat.qualifiers['product'][0]
            mat = pat.search(product)
            if mat is not None:
                remove_list.append(feat)
        for feat in remove_list:
            match.features.remove(feat)
        if match.features != []:
            matches.append(match)
    return matches


def filter_for_self_matches(match_list):
    """only keep matches that have a similar stem loop to another match"""
    from Levenshtein import distance

    hits_by_loop = {}
    for hit in match_list:
        loop = hit.get_loop()
        if hits_by_loop.has_key(loop):
            hits_by_loop[loop].append(hit)
        else:
            hits_by_loop[loop] = [hit]

    new_matches = []

    for key in hits_by_loop.keys():
        num_seqs = len(hits_by_loop[key])
        logging.info("Found %s sequences with loop %r" % (num_seqs, key))
        print "Found %s sequences with loop %r" % (num_seqs, key)
        loop_hits = hits_by_loop[key]
        for i in range(0, num_seqs - 1):
            for j in range(i + 1, num_seqs):
                first = "%s%s%s" % (loop_hits[i].get_before(),
                                    loop_hits[i].get_loop(),
                                    loop_hits[i].get_after())
                second = "%s%s%s" % (loop_hits[j].get_before(),
                                     loop_hits[j].get_loop(),
                                     loop_hits[j].get_after())
                dist = distance(first, second)
                if dist < 2:
                    if not loop_hits[i] in new_matches:
                        new_matches.append(loop_hits[i])
                    if not loop_hits[j] in new_matches:
                        new_matches.append(loop_hits[j])
                    print "%r(%s:%s) <-> %r(%s:%s): %s" % (first,
                                                           loop_hits[i].start(), loop_hits[i].end(),
                                                           second,
                                                           loop_hits[j].start(), loop_hits[j].end(),
                                                           dist)

    return new_matches


def filter_same_position(match_list):
    """Filter out matches where there """
    for m in match_list:
        for f in m.features:
            for aln in f.n_align:
                if not is_same_position(f, aln):
                    f.n_align.remove(aln)
            for aln in f.p_align:
                if not is_same_position(f, aln):
                    f.p_align.remove(aln)
    return match_list


def filter_same_loop_sequence(match_list):
    """Filter out matches where the only alignments have different loop sequences"""
    for m in match_list:
        for f in m.features:
            for aln in f.n_align:
                if not is_same_loop_sequence(m.get_loop(), aln):
                    print >> sys.stderr, "Removing mismatched p_aln %r" % aln.title
                    f.n_align.remove(aln)
            for aln in f.p_align:
                if not is_same_loop_sequence(m.get_loop(), aln):
                    print >> sys.stderr, "Removing mismatched n_aln %r" % aln.title
                    f.p_align.remove(aln)
    return match_list


def filter_downstream_only(match_list):
    for match in match_list:
        for f in match.features:
            if not f.position.startswith('downstream'):
                match.features.remove(f)
    return match_list


def calculate_stats(matches):
    """Calculate stats for the different loop sequences"""
    stats = {}
    for hit in matches:
        loop = str(hit.get_loop())
        if stats.has_key(loop):
            stats[loop] += 1
        else:
            stats[loop] = 1

    print "Statistics:\nLoop seq\tcount\n--------\t-----"
    for key in sorted(stats.keys()):
        print "%s\t\t%s" % (key, stats[key])


def process_sequence(sequence, forward_only=False):
    # Find our pattern in the genome

    forward_pattern = re.compile(FORWARD_PATTERN)
    forward_matches = find_matches(sequence, forward_pattern, FORWARD)
    matches = forward_matches
    forward_hits = len(forward_matches)

    if not forward_only:
        reverse_pattern = re.compile(REVERSE_PATTERN)
        reverse_matches = find_matches(sequence, reverse_pattern, REVERSE)
        matches.extend(reverse_matches)
    else:
        reverse_matches = []

    print "Found %s forward, %s reverse matches" % (forward_hits,
                                                    len(reverse_matches))
    return matches
