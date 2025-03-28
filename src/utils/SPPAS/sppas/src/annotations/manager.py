"""
    ..
        ---------------------------------------------------------------------
         ___   __    __    __    ___
        /     |  \  |  \  |  \  /              the automatic
        \__   |__/  |__/  |___| \__             annotation and
           \  |     |     |   |    \             analysis
        ___/  |     |     |   | ___/              of speech

        http://www.sppas.org/

        Use of this software is governed by the GNU Public License, version 3.

        SPPAS is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        SPPAS is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with SPPAS. If not, see <http://www.gnu.org/licenses/>.

        This banner notice must not be removed.

        ---------------------------------------------------------------------

    src.annotations.manager.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

import logging
import traceback
import sys
import json
import os
from threading import Thread

from sppas import paths
from sppas.src.utils.fileutils import sppasFileUtils
from sppas.src.anndata import sppasTranscription, sppasRW

import sppas.src.audiodata.aio
import sppas.src.anndata.aio
from sppas.src.annotations.infotier import sppasMetaInfoTier
from sppas.src.annotations.log import sppasLog

from sppas.src.annotations.Momel.sppasmomel import sppasMomel
from sppas.src.annotations.Intsint.sppasintsint import sppasIntsint
from sppas.src.annotations.SearchIPUs.sppassearchipus import sppasSearchIPUs
from sppas.src.annotations.FillIPUs.sppasfillipus import sppasFillIPUs
from sppas.src.annotations.TextNorm.sppastextnorm import sppasTextNorm
from sppas.src.annotations.Phon.sppasphon import sppasPhon
from sppas.src.annotations.Align.sppasalign import sppasAlign
from sppas.src.annotations.Syll.sppassyll import sppasSyll
from sppas.src.annotations.TGA.sppastga import sppasTGA
from sppas.src.annotations.SelfRepet.sppasrepet import sppasSelfRepet

# ----------------------------------------------------------------------------


class sppasAnnotationsManager(Thread):
    """Parent class for running annotation processes.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2019  Brigitte Bigi

    Run annotations on a set of files.

    """

    def __init__(self):
        """Create a new sppasAnnotationsManager instance.

        Initialize a Thread.

        """
        Thread.__init__(self)

        # fix members that are required to run annotations
        self._parameters = None
        self._progress = None
        self._logfile = sppasLog()

        # fix optional members
        self.__do_merge = False

        # fix annotations: key,instance
        self._annotations = self.__parse_config_file()

        # start threading
        self.start()

    # ------------------------------------------------------------------------

    def __parse_config_file(self):
        """Parse the sppasui.json file.

        Parse the file to get the list of annotations.

        """
        config = os.path.join(paths.etc, "sppasui.json")
        if os.path.exists(config) is False:
            raise IOError('Installation error: the file to configure the '
                          'automatic annotations does not exist.')

        # Read the whole file content
        with open(config) as cfg:
            dict_cfg = json.load(cfg)

        return dict_cfg["annotate"]

    # -----------------------------------------------------------------------
    # Options of the manager
    # -----------------------------------------------------------------------

    def set_do_merge(self, do_merge):
        """Fix if the 'annotate' method have to create a merged file or not.

        :param do_merge: (bool) if set to True, a merged file will be created

        """
        self.__do_merge = do_merge

    # ------------------------------------------------------------------------
    # Run annotations
    # ------------------------------------------------------------------------

    def annotate(self, parameters, progress=None):
        """Run activated annotations.

        Get execution information from the 'parameters' object.
        Create a Procedure Outcome Report if a filename is set in the
        parameters.

        """
        self._parameters = parameters
        self._progress = progress

        # Print header message in the log-report file or in the logging
        report_file = self._parameters.get_report_filename()
        if report_file:
            try:
                self._logfile = sppasLog(self._parameters)
                self._logfile.create(report_file)
            except:
                self._logfile = sppasLog()
        self._logfile.print_header()
        self._logfile.print_annotations_header()

        # Run all enabled annotations
        ann_stats = [-1] * self._parameters.get_step_numbers()
        steps = False

        for i in range(self._parameters.get_step_numbers()):

            # ignore disabled annotations
            if self._parameters.get_step_status(i) is False:
                continue

            # ok, this annotation is enabled.
            annotation_key = self._parameters.get_step_key(i)
            self._logfile.print_step(i)

            if steps is False:
                steps = True
            elif self._progress:
                self._progress.set_new()

            try:

                if annotation_key == "fillipus":
                    ann_stats[i] = self._run_fillipus()

                elif annotation_key == "alignment":
                    ann_stats[i] = self._run_alignment()

                else:
                    ann_stats[i] = self._run_annotation(annotation_key)

            except Exception as e:
                self._logfile.print_message(
                    "{:s}\n".format(str(e)), indent=1, status=-1)
                logging.info(traceback.format_exc())
                ann_stats[i] = 0

        # Log file & Merge
        self._logfile.print_separator()
        self._logfile.print_newline()
        if self.__do_merge:
            self._logfile.print_separator()
            self._merge()
        self._logfile.print_stats(ann_stats)
        self._logfile.close()

    # -----------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------------

    def _get_instance(self, annotation_key):
        classname = None
        for a in self._annotations:
            if a['id'] == annotation_key:
                classname = a['api']
                break
        if classname is None:
            raise IOError('Unknown annotation key: {:s}'.format(annotation_key))

        return getattr(sys.modules[__name__], classname)

    # ------------------------------------------------------------------------

    def _create_ann_instance(self, annotation_key):
        """Create and configure an instance of an automatic annotation.

        :param annotation_key: (str) Key of an annotation
        :returns: sppasBaseAnnotation

        """
        # Find the index of this annotation
        step_idx = self._parameters.get_step_idx(annotation_key)

        # Create the instance and fix options
        options = self._parameters.get_options(step_idx)
        auto_annot = self._get_instance(annotation_key)(self._logfile)
        if len(options) > 0:
            auto_annot.fix_options(options)

        # Load language resources
        if self._progress:
            self._progress.set_text("Loading resources...")
        step = self._parameters.get_step(step_idx)
        auto_annot.load_resources(*step.get_langresource(), 
                                  lang=step.get_lang())

        return auto_annot

    # -----------------------------------------------------------------------

    def _run_annotation(self, annotation_key):
        """Execute the automatic annotation.

        :param annotation_key: (str) Key of an annotation
        :returns: number of files processed successfully

        """
        a = self._create_ann_instance(annotation_key)
        return a.batch_processing(
            self.get_annot_files(pattern=a.get_input_pattern(),
                                 extensions=a.get_input_extensions()),
            self._progress,
            self._parameters.get_output_format())

    # -----------------------------------------------------------------------

    def _run_fillipus(self):
        """Execute the FillIPUs automatic annotation.

        Requires an audio file with only one channel and its transcription.

        :returns: number of files processed successfully

        """
        a = self._create_ann_instance("fillipus")

        files = list()
        audio_files = self.get_annot_files(
            pattern=a.get_input_pattern(),
            extensions=sppas.src.audiodata.aio.extensions)

        for f in audio_files:
            in_name = os.path.splitext(f)[0] + ".txt"
            files.append((f, in_name))

        return a.batch_processing(
            files,
            self._progress,
            self._parameters.get_output_format())

    # ------------------------------------------------------------------------

    def _run_alignment(self):
        """Execute the Alignment automatic annotation.

        Requires an audio file.
        Requires a phonetization time-aligned with the IPUs.
        Optional: a text-normalization time-aligned with the IPUs.

        :returns: number of files processed successfully

        """
        a = self._create_ann_instance("alignment")

        audio_files = self.get_annot_files(
            pattern="", extensions=sppas.src.audiodata.aio.extensions)

        files = list()
        for f in audio_files:

            # Get the input file
            extt = ['-token' + self._parameters.get_output_format()]
            extp = [a.get_input_pattern() + self._parameters.get_output_format()]
            for e in sppas.src.anndata.aio.extensions_out:
                extt.append('-token' + e)
                extp.append(a.get_input_pattern() + e)

            phon = self._get_filename(f, extp)
            tok = self._get_filename(f, extt)
            if phon is not None:
                files.append(((f, phon), tok))

        return a.batch_processing(
            files,
            self._progress,
            self._parameters.get_output_format())

    # -----------------------------------------------------------------------
    # Manage annotations:
    # -----------------------------------------------------------------------

    def __add_trs(self, trs, trs_inputfile):

        try:
            parser = sppasRW(trs_inputfile)
            trs_input = parser.read(trs_inputfile)
        except IOError:
            return 0

        for tier in trs_input:
            already_in = False
            if trs.is_empty() is False:
                tier_name = tier.get_name()
                for t in trs:
                    if t.get_name() == tier_name:
                        already_in = True
            if already_in is False:
                trs.append(tier)
        return 1

    # ------------------------------------------------------------------------

    def _merge(self):
        """Merge all annotated files."""
        self._progress.set_header("Merge all annotations in a file")
        self._progress.update(0, "")

        # Get the list of files with the ".wav" extension
        filelist = self.get_annot_files(
            pattern="", extensions=sppas.src.audiodata.aio.extensions)
        total = len(filelist)

        output_format = self._parameters.get_output_format()

        for i, f in enumerate(filelist):

            nbfiles = 0

            # Change f, to allow "replace" to work properly
            basef = os.path.splitext(f)[0]

            self._logfile.print_message("File: " + f, indent=0)
            self._progress.set_text(os.path.basename(f)+" ("+str(i+1)+"/"+str(total)+")")

            # Add all files content in the same order than to annotate
            trs = sppasTranscription()
            nbfiles += self.__add_trs(trs, basef + output_format)
            for s in range(self._parameters.get_step_numbers()):
                ann_key = self._parameters.get_step_key(s)
                a = self._get_instance(ann_key)
                pattern = a.get_pattern()
                if len(pattern) > 0:
                    nbfiles += self.__add_trs(trs, basef + pattern + output_format)

            if nbfiles > 1:
                try:
                    info_tier = sppasMetaInfoTier(trs)
                    tier = info_tier.create_time_tier(
                        trs.get_min_loc().get_midpoint(),
                        trs.get_max_loc().get_midpoint())
                    trs.append(tier)
                    parser = sppasRW(basef + "-merge.xra")
                    parser.write(trs)
                    self._logfile.print_message(
                        basef + "-merge.xra", indent=1, status=0)

                except Exception as e:
                    self._logfile.print_message(str(e), indent=1, status=-1)

            self._progress.set_fraction(float((i+1))/float(total))
            self._logfile.print_newline()

        self._progress.update(1, "Completed.")
        self._progress.set_header("")

    # -----------------------------------------------------------------------
    # Manage files:
    # -----------------------------------------------------------------------

    def get_annot_files(self, pattern, extensions):
        """Search for annotated files with pattern and extensions.

        :param pattern: (str) The pattern to search in the inputs
        :param extensions: (str) The extension to search
        :returns: List of filenames matching pattern and extensions

        """
        files = list()

        if len(pattern) > 0:
            ext = [pattern + self._parameters.get_output_format()]
            for e in extensions:
                ext.append(pattern + e)
        else:
            ext = extensions

        for f in self._parameters.get_sppasinput():
            new_file = self._get_filename(f, ext)
            if new_file is not None and new_file not in files:
                files.append(new_file)

        return files

    # ------------------------------------------------------------------------

    def _get_filename(self, filename, extensions):
        """Return a filename corresponding to one of extensions.

        :param filename: input file name
        :param extensions: the list of expected extension
        :returns: a file name of the first existing file with an expected
        extension or None

        """
        base_name = os.path.splitext(filename)[0]
        for ext in extensions:
            ext_filename = base_name + ext
            new_filename = sppasFileUtils(ext_filename).exists()
            if new_filename is not None and os.path.isfile(new_filename):
                return new_filename

        return None
