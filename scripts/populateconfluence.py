#!/usr/bin/env python3

# Import ATC classes
from scripts.dataneeded import DataNeeded
from scripts.detectionrule import DetectionRule
from scripts.mitigationsystem import MitigationSystem
from scripts.mitigationpolicy import MitigationPolicy
from scripts.hardeningpolicy import HardeningPolicy
from scripts.loggingpolicy import LoggingPolicy
from scripts.triggers import Triggers
from scripts.enrichment import Enrichment
from scripts.customer import Customer
from scripts.attack_mapping import te_mapping
from scripts.init_confluence import main as init_main
from scripts.usecases import Usecase

# Import ATC Utils
from scripts.atcutils import ATCutils

# Others
import glob
import sys
import traceback
import os

ATCconfig = ATCutils.load_config("config.yml")


class PopulateConfluence:
    """Desc"""

    def __init__(self, auth, lp=False, dn=False, dr=False, en=False, tg=False,
                 cu=False, ms=False, mp=False, hp=False, auto=False, uc=False,
                 art_dir=False, atc_dir=False, lp_path=False, dn_path=False, 
                 dr_path=False, en_path=False, tg_path=False, cu_path=False, 
                 hp_path=False, ms_path=False, mp_path=False, uc_path=False, 
                 init=False):
        """Desc"""

        self.auth = auth

        self.space = ATCconfig.get('confluence_space_name')
        self.apipath = ATCconfig.get('confluence_rest_api_url')
        self.root_name = ATCconfig.get('confluence_name_of_root_directory')

        # Check if atc_dir provided
        if atc_dir:
            self.atc_dir = atc_dir

        else:
            self.atc_dir = ATCconfig.get('md_name_of_root_directory')

        # Check if art_dir provided
        if art_dir:
            self.art_dir = art_dir

        else:
            self.art_dir = ATCconfig.get('triggers_directory')

        # Check if init switch is used
        if init:
            if init_main(self.auth):
                print("[+] Created initial confluence pages successfully")
            else:
                print("[-] Failed to create initial confluence pages")
                raise Exception("Failed to init pages")

        # Main logic
        if auto:
            self.hardening_policy(hp_path)
            self.mitigation_system(ms_path)
            self.mitigation_policy(mp_path)
            self.logging_policy(lp_path)
            self.data_needed(dn_path)
            self.enrichment(en_path)
            self.triggers(tg_path)
            self.detection_rule(dr_path)
            self.customer(cu_path)
            self.usecases(uc_path)

        if hp:
            self.hardening_policy(hp_path)

        if ms:
            self.mitigation_system(ms_path)

        if mp:
            self.mitigation_policy(mp_path)
        
        if lp:
            self.logging_policy(lp_path)

        if dn:
            self.data_needed(dn_path)

        if en:
            self.enrichment(en_path)

        if dr:
            self.detection_rule(dr_path)

        if tg:
            self.triggers(tg_path)

        if cu:
            self.customer(cu_path)

        if uc:
            self.usecases(uc_path)

    def triggers(self, tg_path):
        """Populate Triggers"""

        print("[*] Populating Triggers...")
        if tg_path:
            tg_list = glob.glob(tg_path + '*.yml')
        else:
            tg_list = glob.glob(ATCconfig.get("triggers_directory") +
                                '/T*/*.yaml')

        for tg_file in tg_list:
            try:
                tg = Triggers(tg_file)
                tg.render_template("confluence")
                title = tg.fields["attack_technique"] + ": " + \
                    te_mapping.get(tg.fields["attack_technique"])
                confluence_data = {
                    "title": title,
                    "spacekey": self.space,
                    "parentid": str(ATCutils.confluence_get_page_id(
                        self.apipath, self.auth, self.space, "Triggers")),
                    "confluencecontent": tg.content,
                }

                res = ATCutils.push_to_confluence(confluence_data, self.apipath,
                                            self.auth)
                if res == 'Page updated':
            	    print("==> updated page: TR '" + title + "'")
                # print("Done: ", tg.fields["attack_technique"])
            except Exception as err:
                print(tg_file + " failed")
                print("Err message: %s" % err)
                print('-' * 60)
                traceback.print_exc(file=sys.stdout)
                print('-' * 60)

        print("[+] Triggers populated!")

    def hardening_policy(self, hp_path):
        """Populate Hardening Policies"""

        print("[*] Populating Hardening Policies...")
        if hp_path:
            hp_list = glob.glob(hp_path + '*.yml')
        else:
            hp_dir = ATCconfig.get('hardening_policies_directory')
            hp_list = glob.glob(hp_dir + '/*.yml')

        for hp_file in hp_list:
            try:
                hp = HardeningPolicy(hp_file)
                hp.render_template("confluence")
                confluence_data = {
                    "title": hp.hp_parsed_file["title"],
                    "spacekey": self.space,
                    "parentid": str(ATCutils.confluence_get_page_id(
                        self.apipath, self.auth, self.space,
                        "Hardening Policies")),
                    "confluencecontent": hp.content,
                }

                res = ATCutils.push_to_confluence(confluence_data, self.apipath,
                                            self.auth)
                if res == 'Page updated':
            	    print("==> updated page: HP '" + hp.hp_parsed_file['title'] + "'")
            except Exception as err:
                print(hp_file + " failed")
                print("Err message: %s" % err)
                print('-' * 60)
                traceback.print_exc(file=sys.stdout)
                print('-' * 60)
        print("[+] Hardening Policies populated!")

    def mitigation_system(self, ms_path):
        """Populate Mitigation Systems"""

        print("[*] Populating Mitigation Systems...")
        if ms_path:
            ms_list = glob.glob(ms_path + '*.yml')
        else:
            ms_dir = ATCconfig.get('mitigation_systems_directory')
            ms_list = glob.glob(ms_dir + '/*.yml')

        for ms_file in ms_list:
            try:
                ms = MitigationSystem(ms_file)
                ms.render_template("confluence")
                confluence_data = {
                    "title": ms.ms_parsed_file["title"],
                    "spacekey": self.space,
                    "parentid": str(ATCutils.confluence_get_page_id(
                        self.apipath, self.auth, self.space,
                        "Mitigation Systems")),
                    "confluencecontent": ms.content,
                }

                res = ATCutils.push_to_confluence(confluence_data, self.apipath,
                                            self.auth)
                if res == 'Page updated':
            	    print("==> updated page: MS '" + ms.ms_parsed_file['title'] + "'")
            except Exception as err:
                print(ms_file + " failed")
                print("Err message: %s" % err)
                print('-' * 60)
                traceback.print_exc(file=sys.stdout)
                print('-' * 60)
        print("[+] Mitigation Systems populated!")

    def mitigation_policy(self, mp_path):
        """Populate Mitigation Policies"""

        print("[*] Populating Mitigation Policies...")
        if mp_path:
            mp_list = glob.glob(mp_path + '*.yml')
        else:
            mp_dir = ATCconfig.get('mitigation_policies_directory')
            mp_list = glob.glob(mp_dir + '/*.yml')

        for mp_file in mp_list:
            try:
                mp = MitigationPolicy(mp_file, apipath=self.apipath,
                               auth=self.auth, space=self.space)
                mp.render_template("confluence")
                confluence_data = {
                    "title": mp.mp_parsed_file["title"],
                    "spacekey": self.space,
                    "parentid": str(ATCutils.confluence_get_page_id(
                        self.apipath, self.auth, self.space,
                        "Mitigation Policies")),
                    "confluencecontent": mp.content,
                }

                res = ATCutils.push_to_confluence(confluence_data, self.apipath,
                                            self.auth)
                if res == 'Page updated':
            	    print("==> updated page: MP '" + mp.mp_parsed_file['title'] + "'")
            except Exception as err:
                print(mp_file + " failed")
                print("Err message: %s" % err)
                print('-' * 60)
                traceback.print_exc(file=sys.stdout)
                print('-' * 60)
        print("[+] Mitigation Policies populated!")

    def logging_policy(self, lp_path):
        """Desc"""

        print("[*] Populating Logging Policies...")
        if lp_path:
            lp_list = glob.glob(lp_path + '*.yml')
        else:
            lp_dir = ATCconfig.get('logging_policies_dir')
            lp_list = glob.glob(lp_dir + '/*.yml')

        for lp_file in lp_list:
            try:
                lp = LoggingPolicy(lp_file)
                lp.render_template("confluence")
                confluence_data = {
                    "title": lp.fields["title"],
                    "spacekey": self.space,
                    "parentid": str(ATCutils.confluence_get_page_id(
                        self.apipath, self.auth, self.space,
                        "Logging Policies")),
                    "confluencecontent": lp.content,
                }

                res = ATCutils.push_to_confluence(confluence_data, self.apipath,
                                            self.auth)
                if res == 'Page updated':
            	    print("==> updated page: LP '" + lp.fields['title'] + "'")
                # print("Done: ", lp.fields['title'])
            except Exception as err:
                print(lp_file + " failed")
                print("Err message: %s" % err)
                print('-' * 60)
                traceback.print_exc(file=sys.stdout)
                print('-' * 60)
        print("[+] Logging Policies populated!")

    def data_needed(self, dn_path):
        """Desc"""

        print("[*] Populating Data Needed...")
        if dn_path:
            dn_list = glob.glob(dn_path + '*.yml')
        else:
            dn_dir = ATCconfig.get('data_needed_dir')
            dn_list = glob.glob(dn_dir + '/*.yml')

        for dn_file in dn_list:
            try:
                dn = DataNeeded(dn_file, apipath=self.apipath, auth=self.auth,
                                space=self.space)
                dn.render_template("confluence")
                confluence_data = {
                    "title": dn.dn_fields["title"],
                    "spacekey": self.space,
                    "parentid": str(ATCutils.confluence_get_page_id(
                        self.apipath, self.auth, self.space, "Data Needed")),
                    "confluencecontent": dn.content,
                }

                res = ATCutils.push_to_confluence(confluence_data, self.apipath,
                                            self.auth)
                if res == 'Page updated':
            	    print("==> updated page: DN '" + dn.dn_fields['title'] + "'")
                # print("Done: ", dn.dn_fields['title'])
            except Exception as err:
                print(dn_file + " failed")
                print("Err message: %s" % err)
                print('-' * 60)
                traceback.print_exc(file=sys.stdout)
                print('-' * 60)
        print("[+] Data Needed populated!")

    def detection_rule(self, dr_path):
        """Desc"""

        print("[*] Populating Detection Rules...")
        if dr_path:
            dr_list = glob.glob(dr_path + '*.yml')
        else:
            dr_dirs = ATCconfig.get('detection_rules_directories')
            # check if config provides multiple directories for detection rules
            if isinstance(dr_dirs, list):
                dr_list = []
                for directory in dr_dirs:
                    dr_list += glob.glob(directory + '/*.yml')
            elif isinstance(dr_dirs, str):
                dr_list = glob.glob(dr_dirs + '/*.yml')

        for dr_file in dr_list:
            try:
                dr = DetectionRule(dr_file, apipath=self.apipath,
                                   auth=self.auth, space=self.space
                                   )
                dr.render_template("confluence")

                confluence_data = {
                    "title": dr.fields['title'],
                    "spacekey": self.space,
                    "parentid": str(ATCutils.confluence_get_page_id(
                        self.apipath, self.auth, self.space,
                        "Detection Rules")), "confluencecontent": dr.content,
                }

                res = ATCutils.push_to_confluence(confluence_data, self.apipath,
                                            self.auth)
                if res == 'Page updated':
            	    print("==> updated page: DR '" + dr.fields['title'] + "' (" + dr_file + ")")
                # print("Done: ", dr.fields['title'])
            except Exception as err:
                print(dr_file + " failed")
                print("Err message: %s" % err)
                print('-' * 60)
                traceback.print_exc(file=sys.stdout)
                print('-' * 60)
        print("[+] Detection Rules populated!")

    def enrichment(self, en_path):
        """Nothing here yet"""

        print("[*] Populating Enrichments...")
        if en_path:
            en_list = glob.glob(en_path + '*.yml')
        else:
            en_dir = ATCconfig.get('enrichments_directory')
            en_list = glob.glob(en_dir + '/*.yml')

        for en_file in en_list:
            try:
                en = Enrichment(en_file, apipath=self.apipath,
                                auth=self.auth, space=self.space)
                en.render_template("confluence")

                confluence_data = {
                    "title": en.en_parsed_file['title'],
                    "spacekey": self.space,
                    "parentid": str(ATCutils.confluence_get_page_id(
                        self.apipath, self.auth, self.space,
                        "Enrichments")), "confluencecontent": en.content,
                }

                res = ATCutils.push_to_confluence(confluence_data, self.apipath,
                                            self.auth)
                if res == 'Page updated':
            	    print("==> updated page: EN '" + en.en_parsed_file['title'] + "'")
                # print("Done: ", en.en_parsed_file['title'])
            except Exception as err:
                print(en_file + " failed")
                print("Err message: %s" % err)
                print('-' * 60)
                traceback.print_exc(file=sys.stdout)
                print('-' * 60)
        print("[+] Enrichments populated!")

    def customer(self, cu_path):
        """Nothing here yet"""

        print("[+] Populating Customers...")
        if cu_path:
            cu_list = glob.glob(cu_path + '*.yml')
        else:
            cu_dir = ATCconfig.get('customers_directory')
            cu_list = glob.glob(cu_dir + '/*.yml')

        for cu_file in cu_list:
            try:
                cu = Customer(cu_file, apipath=self.apipath,
                              auth=self.auth, space=self.space)
                cu.render_template("confluence")

                confluence_data = {
                    "title": cu.customer_name,
                    "spacekey": self.space,
                    "parentid": str(ATCutils.confluence_get_page_id(
                        self.apipath, self.auth, self.space,
                        "Customers")),
                    "confluencecontent": cu.content,
                    "metadata": {
                        "labels": [{
                        "name": "atc_customer"
                        }]
                    }
                }

                res = ATCutils.push_to_confluence(confluence_data, self.apipath,
                                            self.auth)
                if res == 'Page updated':
            	    print("==> updated page: CU '" + cu.customer_name + "'")
                # print("Done: ", cu.title)
            except Exception as err:
                print(cu_file + " failed")
                print("Err message: %s" % err)
                print('-' * 60)
                traceback.print_exc(file=sys.stdout)
                print('-' * 60)
        print("[+] Customers populated!")

    def usecases(self, uc_path):
        """Nothing here yet"""

        print("[+] Populating UseCases...")
        if uc_path:
            uc_list = glob.glob(uc_path + '*.yml')
        else:
            uc_dir = ATCconfig.get('usecases_directory')
            uc_list = glob.glob(uc_dir + '/*.yml')

        for uc_file in uc_list:
            try:
                uc = Usecase(uc_file, apipath=self.apipath,
                              auth=self.auth, space=self.space)
                uc.render_template("confluence")

                confluence_data = {
                    "title": uc.title,
                    "spacekey": self.space,
                    "parentid": str(ATCutils.confluence_get_page_id(
                        self.apipath, self.auth, self.space,
                        "Use Cases")),
                    "confluencecontent": uc.content
                }

                res = ATCutils.push_to_confluence(confluence_data, self.apipath,
                                            self.auth)
                if res == 'Page updated':
                    print("==> updated page: UC '" + uc.usecase_name + "'")
                # print("Done: ", cu.title)
            except Exception as err:
                print(uc_file + " failed")
                print("Err message: %s" % err)
                print('-' * 60)
                traceback.print_exc(file=sys.stdout)
                print('-' * 60)
        print("[+] UseCases populated!")
