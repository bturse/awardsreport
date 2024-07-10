from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from typing import Optional
from datetime import date

from awardsreport.database import Base


class HasId:
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class TransactionsMixin:
    action_date: Mapped[Optional[date]] = mapped_column(
        doc="""The date the action being reported was issued / signed by the
        Government or a binding agreement was reached."""
    )
    awarding_agency_code: Mapped[Optional[str]] = mapped_column(
        doc="""Code for agency which made the award. See
        <https://files.usaspending.gov/reference_data/agency_codes.csv> CGAC
        AGENCY CODE column"""
    )
    awarding_agency_name: Mapped[Optional[str]] = mapped_column(
        doc="""The name associated with a department or establishment of the
        Government as used in the Treasury Account Fund Symbol (TAFS). See See
        https://files.usaspending.gov/reference_data/agency_codes.csv (AGENCY
        NAME column)."""
    )
    awarding_office_code: Mapped[Optional[str]] = mapped_column(
        doc="""Identifier of the level n organization that awarded, executed or
        is otherwise responsible for the transaction. See
        https://open.gsa.gov/api/fh-fouo-api/ and
        https://sam.gov/content/hierarchy"""
    )
    awarding_office_name: Mapped[Optional[str]] = mapped_column(
        doc="""Name of the level n organization that awarded, executed or is
        otherwise responsible for the transaction. See 
        https://open.gsa.gov/api/fh-fouo-api/ and
        https://sam.gov/content/hierarchy"""
    )
    awarding_sub_agency_name: Mapped[Optional[str]] = mapped_column(
        doc="""Name of the level 2 organization that awarded, executed or is
        otherwise responsible for the transaction.  See
        https://files.usaspending.gov/reference_data/agency_codes.csv (SUBTIER
        NAME column)"""
    )
    federal_action_obligation: Mapped[Optional[float]] = mapped_column(
        doc="""Amount of Federal government's obligation, de-obligation, or
        liability, in dollars, for an award transaction. The most common value
        used to measure the federal spending of a transaction for non-loans."""
    )
    funding_agency_code: Mapped[Optional[str]] = mapped_column(
        doc="""The 3-digit CGAC agency code of the department or establishment
        of the Government that provided the preponderance of the funds for an
        award and/or individual transactions related to an award. See
        https://files.usaspending.gov/reference_data/agency_codes.csv (CGAC
        AGENCY CODE column)"""
    )
    funding_agency_name: Mapped[Optional[str]] = mapped_column(
        doc="""Name of the department or establishment of the Government that
        provided the preponderance of the funds for an award and/or individual
        transactions related to an award. See
        https://files.usaspending.gov/reference_data/agency_codes.csv (AGENCY
        NAME column)"""
    )
    funding_office_code: Mapped[Optional[str]] = mapped_column(
        doc="""Identifier of the level n organization that provided the
        preponderance of the funds obligated by this transaction. See
        https://open.gsa.gov/api/fh-fouo-api/ and
        https://sam.gov/content/hierarchy"""
    )
    funding_office_name: Mapped[Optional[str]] = mapped_column(
        doc="""Name of the level n organization that provided the preponderance
        of the funds obligated by this transaction. See
        https://open.gsa.gov/api/fh-fouo-api/ and
        https://sam.gov/content/hierarchy"""
    )
    funding_sub_agency_code: Mapped[Optional[str]] = mapped_column(
        doc="""Identifier of the level 2 organization that provided the
        preponderance of the funds obligated by this transaction.  See
        https://files.usaspending.gov/reference_data/agency_codes.csv (SUBTIER
        CODE column)
        """
    )
    funding_sub_agency_name: Mapped[Optional[str]] = mapped_column(
        doc="""Name of the level 2 organization that provided the preponderance
        of the funds obligated by this transaction.  See
        https://files.usaspending.gov/reference_data/agency_codes.csv (SUBTIER
        NAME column) 
        """
    )
    initial_report_date: Mapped[Optional[date]] = mapped_column(
        doc="""Date transaction was originally reported in USAspending source system."""
    )
    last_modified_date: Mapped[Optional[date]] = mapped_column(
        doc="""Date transaction was most recently modified in USAspending source system."""
    )
    period_of_performance_current_end_date: Mapped[Optional[date]] = mapped_column(
        doc="""For procurement awards: The contract completion date based on the
        schedule in the contract. For an initial award, this is the scheduled
        completion date for the base contract and for any options exercised at
        time of award. For modifications that exercise options or that shorten
        (such as termination) or extend the contract period of performance, this
        is the revised scheduled completion date for the base contract including
        exercised options. If the award is solely for the purchase of supplies
        to be delivered, the completion date should correspond to the latest
        delivery date on the base contract and any exercised options. The
        completion date does not change to reflect a closeout date. 

        For grants and cooperative agreements: The Period of Performance is
        defined in the CFR 200 as the total estimated time interval between the
        start of an initial Federal award and the planned end date, which may
        include one or more funded portions, or budget periods. If the end date
        is revised due to an extension, termination, lack of available funds, or
        other reason, the current end date will be amended.

        For all other financial assistance awards: The current date on which,
        for the award referred to by the action being reported, awardee effort
        completes or the award is otherwise ended. Administrative actions
        related to this award may continue to occur after this date.
        """
    )
    period_of_performance_start_date: Mapped[Optional[date]] = mapped_column(
        doc="""For procurement awards: Per the FPDS data dictionary, the date that
        the parties agree will be the starting date for the contract's
        requirements. This is the period of performance start date for the
        entire contract period, this date does not reflect period of performance
        per modification, but rather the start of the entire contract period of
        performance. This data element does NOT correspond to FAR 43.101 or
        52.243 and should not be mapped to those fields in your contract writing
        systems. 

        For grants and cooperative agreements: The Period of Performance is
        defined in the 2 CFR 200 as the total estimated time interval between
        the start of an initial Federal award and the planned end date, which
        may include one or more funded portions, or budget periods.

        For all other financial assistance awards: The date on which, for the
        award referred to by the action being reported, awardee effort begins or
        the award is otherwise effective."""
    )
    primary_place_of_performance_city_name: Mapped[Optional[str]] = mapped_column(
        doc="""The name of the city where the predominant performance of the
        award will be accomplished.
        
        Subawards and Contracts: refer to the GSA FSRS and FPDS systems
        
        Assistance: see
        https://www.usgs.gov/core-science-systems/ngp/board-on-geographic-names/download-gnis-data
        """
    )
    primary_place_of_performance_country_code: Mapped[Optional[str]] = mapped_column(
        doc="""Country code where the predominant performance of the award will
        be accomplished.
        
        Subawards and Contracts: refer to the GSA FSRS and
        
        FPDS systems Financial Assistance: GENC Standard Version 3, Update 4,
        available from the following source:
        https://nsgreg.nga.mil/genc/discovery?type=gp&field=name&searchText=&day=30&month=6&year=2016
        """
    )
    primary_place_of_performance_country_name: Mapped[Optional[str]] = mapped_column(
        doc="""Name of the country represented by the country code where the
        predominant performance of the award will be accomplished.
        
        Subawards and Contracts: refer to the GSA FSRS and FPDS systems
        
        Financial Assistance: GENC Standard Version 3, Update 4, available from
        the following source:
        https://nsgreg.nga.mil/genc/discovery?type=gp&field=name&searchText=&day=30&month=6&year=2016
        """
    )
    primary_place_of_performance_county_name: Mapped[Optional[str]] = mapped_column(
        doc="""The name of the county where the predominant performance of the
        award will be accomplished. See
        https://geonames.usgs.gov/docs/stategaz/GOVT_UNITS.zip"""
    )
    primary_place_of_performance_state_name: Mapped[Optional[str]] = mapped_column(
        doc="""Primary Place of Performance State. Two-letter abbreviation for
        the state or territory indicating where the predominant performance of
        the award will be accomplished. See
        https://geonames.usgs.gov/docs/stategaz/AllStates.zip"""
    )
    primary_place_of_performance_zip_4: Mapped[Optional[str]] = mapped_column(
        doc="""United States ZIP code (five digits) concatenated with the
        additional +4 digits, identifying where the predominant performance of
        the award will be accomplished.
        
        Data for validation purposes is sourced from USPS Postal Pro, though
        agencies are able to submit +4 ZIP components outside this list with a
        warning when the first five digits are in the Postal Pro file."""
    )
    prime_award_base_transaction_description: Mapped[Optional[str]] = mapped_column(
        doc="""The transaction description of the first transaction on a prime
        award summary. Transaction description definition:
        
        For procurement awards: Per the FPDS data dictionary, a brief, summary
        level, plain English, description of the contract, award, or
        modification. Additional information: the description field may also
        include abbreviations, acronyms, or other information that is not plain
        English such as that required by OMB policies (CARES Act, etc).
        
        For financial assistance awards: A plain language description of the
        Federal award purpose; activities to be performed; deliverables and
        expected outcomes; intended beneficiary(ies); and subrecipient
        activities if known/specified at the time of award."""
    )
    prime_award_transaction_place_of_performance_cd_current: Mapped[Optional[str]] = (
        mapped_column(
            doc="""Congressional district where the predominant performance of the
        award will be accomplished. Based on current congressional district map.

        Derived with a threshold methodology using 9 digit zip, 5 digit zip,
        city, county, and state place of performance information from the
        transaction using the current congressional district map.
        """
        )
    )
    prime_award_transaction_place_of_performance_cd_original: Mapped[Optional[str]] = (
        mapped_column(
            doc="""Congressional district where the predominant performance of the
        award will be accomplished. Based on current congressional district map.

        Values as submitted to or derived by USAspending source system.
        """
        )
    )
    prime_award_transaction_place_of_performance_county_fips_code: Mapped[
        Optional[str]
    ] = mapped_column(
        String(5),
        doc="""5 character county FIPS code consisting of 2 character
        state_numeric code, and 3 character county_numeric code. See Government
        Units file:
        https://www.usgs.gov/us-board-on-geographic-names/download-gnis-datahttps://www.usgs.gov/us-board-on-geographic-names/download-gnis-data.""",
    )
    prime_award_transaction_place_of_performance_state_fips_code: Mapped[
        Optional[str]
    ] = mapped_column(
        doc="""2 digit numeric state identifier code where the predominant
        performance of the award will be accomplished. See
        https://geonames.usgs.gov/docs/stategaz/GOVT_UNITS.zip"""
    )
    prime_award_transaction_recipient_cd_current: Mapped[Optional[str]] = mapped_column(
        doc="""Congressional district of transaction recipient. Based on current
        congressional district map.

        Derived with a threshold methodology using 9 digit zip, 5 digit zip,
        city, county, and state recipient information from the
        transaction using the current congressional district map.
        """
    )
    prime_award_transaction_recipient_cd_original: Mapped[Optional[str]] = (
        mapped_column(
            doc="""Congressional district of transaction recipient. Based on current
        congressional district map.

        Values as submitted to or derived by USAspending source system.
        """
        )
    )
    prime_award_transaction_recipient_county_fips_code: Mapped[Optional[str]] = (
        mapped_column(
            doc="""5 digit numeric county identifier code of transaction recipient.
        See https://geonames.usgs.gov/docs/stategaz/GOVT_UNITS.zip"""
        )
    )
    prime_award_transaction_recipient_state_fips_code: Mapped[Optional[str]] = (
        mapped_column(
            doc="""2 digit numeric state identifier code of transaction recipient.
        See https://geonames.usgs.gov/docs/stategaz/GOVT_UNITS.zip"""
        )
    )
    recipient_address_line_1: Mapped[Optional[str]] = mapped_column(
        doc="""First line of the awardee or recipient's legal business address
        where the office represented by the Unique Entity Identifier (as
        registered in the System for Award Management) is located."""
    )
    recipient_address_line_2: Mapped[Optional[str]] = mapped_column(
        doc="""Second line of awardee or recipient's legal business address."""
    )
    recipient_city_name: Mapped[Optional[str]] = mapped_column(
        doc="""Name of the city in which the awardee or recipient's legal
        business address is located."""
    )
    recipient_country_code: Mapped[Optional[str]] = mapped_column(
        doc="""Code for the country in which the awardee or recipient is
        located, using the International Standard for country codes (ISO) 3166-1
        Alpha-3 GENC Profile, minus the codes listed for those territories and
        possessions of the United States already identified as “states.”

        Subawards and Contracts: refer to the GSA FSRS and FPDS systems

        Financial Assistance: GENC Standard Version 3, Update 4, available from the
        following source:
        https://nsgreg.nga.mil/genc/discovery?type=gp&field=name&searchText=&day=30&month=6&year=2016"""
    )
    recipient_country_name: Mapped[Optional[str]] = mapped_column(
        doc="""The name corresponding to the country code.
        
        Subawards and Contracts: refer to the GSA FSRS and FPDS systems
        
        Financial Assistance: GENC Standard Version 3, Update 4, available from
        the following source:
        https://nsgreg.nga.mil/genc/discovery?type=gp&field=name&searchText=&day=30&month=6&year=2016
        """
    )
    recipient_county_name: Mapped[Optional[str]] = mapped_column(
        doc="""Name of the county in which the awardee or recipient's legal
        business address is located. See
        https://geonames.usgs.gov/docs/stategaz/GOVT_UNITS.zip"""
    )
    recipient_name: Mapped[Optional[str]] = mapped_column(
        doc="""The name of the awardee or recipient that relates to the unique
        identifier. For U.S. based companies, this name is what the business
        ordinarily files in formation documents with individual states (when
        required). See https://sam.gov/content/entity-information"""
    )
    recipient_name_raw: Mapped[Optional[str]]
    recipient_parent_name: Mapped[Optional[str]] = mapped_column(
        doc="""The name of the ultimate parent of the awardee or recipient. See
        https://sam.gov/content/entity-information"""
    )
    recipient_parent_name_raw: Mapped[Optional[str]]
    recipient_parent_uei: Mapped[Optional[str]] = mapped_column(
        doc="""The UniqueEntity Identifier of the ultimate parent of the awardee
        or recipient. See https://sam.gov/content/entity-information"""
    )
    recipient_state_code: Mapped[Optional[str]] = mapped_column(
        doc="""United States Postal Service (USPS) two-letter abbreviation for
        the state or territory in which the awardee or recipient’s legal
        business address is located. Identify States, the District of Columbia,
        territories (i.e., American Samoa, Guam, Northern Mariana Islands,
        Puerto Rico, U.S. Virgin Islands) and associated states (i.e., Republic
        of the Marshall Islands, the Federated States of Micronesia, and Palau)
        by their USPS two-letter abbreviation for the purposes of reporting.

        See https://geonames.usgs.gov/docs/stategaz/AllStates.zip
        """
    )
    recipient_state_name: Mapped[Optional[str]] = mapped_column(
        doc="""State where the awardee or recipient is located."""
    )
    recipient_uei: Mapped[Optional[str]] = mapped_column(
        doc="""The Unique Entity Identifier (UEI) for an awardee or recipient. A
        UEI is a unique alphanumeric code used to identify a specific
        commercial, nonprofit, or business entity. See
        https://www.fsd.gov/gsafsd_sp?id=kb_article_view&sysparm_article=KB0041255 and https://sam.gov/content/entity-information"""
    )
    transaction_description: Mapped[Optional[str]] = mapped_column(
        doc="""For procurement awards: Per the FPDS data dictionary, a brief,
        summary level, plain English, description of the contract, award, or
        modification. Additional information: the description field may also
        include abbreviations, acronyms, or other information that is not plain
        English such as that required by OMB policies (CARES Act, etc).
        
        For financial assistance awards: A plain language description of the
        Federal award purpose; activities to be performed; deliverables and
        expected outcomes; intended beneficiary(ies); and subrecipient
        activities if known/specified at the time of award."""
    )
    usaspending_permalink: Mapped[Optional[str]] = mapped_column(
        doc="""URL of award profile for this record on USAspending.gov"""
    )


class ProcurementTransactionsMixin:
    city_local_government: Mapped[Optional[str]] = mapped_column(
        doc=""""Characteristic of the entity such as whether the selected entity
        is a City Local Government or not. It is derived from the SAM data
        element, 'Business Types'. See
        https://www.fpds.gov/fpdsng_cms/index.php/en/worksite.html"""
    )
    contract_award_unique_key: Mapped[Optional[str]] = mapped_column(
        doc="""Unique key of contract Prime Award Summary. Note that this
        element is different from the ContractTransactionUniqueKey in that it
        identifies the award, not a specific transaction within the award. A
        concatenation of PIID, agencyID, ParentAwardId, and Referenced IDV
        Agency Identifier. A single underscore ('_') character is inserted in
        between each element value. If an element value is blank then the values
        used is "NONE"."""
    )
    contract_transaction_unique_key: Mapped[Optional[str]] = mapped_column(
        doc="""Derived element and system-generated database key used to
        uniquely identify each contract transaction record and facilitate record
        lookup, correction, and deletion. A concatenation of agencyID,
        Referenced IDV Agency Identifier, PIID,
        AwardModificationAmendmentNumber, ParentAwardId, and Transaction Number,
        with a single underscore ('_') character inserted in between each. If a
        field is blank, it is recorded as "-none-". agencyID is an FPDS field
        that captures the Agency or SubTier Agency that submitted the
        transaction to FPDS (often distinct from the awarding agency). For
        contract IDV records, only agencyID, PIID, and
        AwardModificationAmendmentNumber are part of the unique key, even if
        additional fields in the key are present in the IDV record; the rest of
        the fields are recorded as "-none-" for unique key purposes. Example of
        ContractTransactionUniqueKey:
        9700_-none-FA440706C0001_P00007-none-_0."""
    )
    county_local_government: Mapped[Optional[str]] = mapped_column(
        doc=""""Characteristic of the entity such as whether the selected entity
        is a County Local Government or not. It is derived from the SAM data
        element, 'Business Types'. See
        https://www.fpds.gov/fpdsng_cms/index.php/en/worksite.html"""
    )
    domestic_or_foreign_entity: Mapped[Optional[str]] = mapped_column(
        doc="""See
        https://www.fpds.gov/fpdsng_cms/index.php/en/worksite.html"""
    )
    domestic_or_foreign_entity_code: Mapped[Optional[str]] = mapped_column(
        doc="""See
        https://www.fpds.gov/fpdsng_cms/index.php/en/worksite.html"""
    )
    inter_municipal_local_government: Mapped[Optional[str]] = mapped_column(
        doc="""Characteristic of the entity such as whether the selected entity
        is an Inter-Municipal Local Government or not. It is derived from the
        SAM data element, 'Business Types'. See
        https://www.fpds.gov/fpdsng_cms/index.php/en/worksite.html"""
    )
    local_government_owned: Mapped[Optional[str]] = mapped_column(
        doc="""Characteristic of the entity such as whether the selected entity
        is a Local Government Owned or not. It is derived from the SAM data
        element, 'Business Types'. See
        https://www.fpds.gov/fpdsng_cms/index.php/en/worksite.html"""
    )
    municipality_local_government: Mapped[Optional[str]] = mapped_column(
        doc="""Characteristic of the entity such as whether the selected entity
        is a Municipality Local Government or not. It is derived from the SAM data
        element, 'Business Types'. See
        https://www.fpds.gov/fpdsng_cms/index.php/en/worksite.html"""
    )
    naics_code: Mapped[Optional[str]] = mapped_column(
        doc="""The identifier that represents the North American Industrial
        Classification System (NAICS) Code assigned to the solicitation and
        resulting award identifying the industry in which the contract
        requirements are normally performed. See
        https://www.census.gov/naics/"""
    )
    naics_description: Mapped[Optional[str]] = mapped_column(
        doc="""The title associated with the NAICS Code. See
        https://www.census.gov/naics/"""
    )
    period_of_performance_potential_end_date: Mapped[Optional[str]] = mapped_column(
        doc="""For procurement, the date on which, for the award referred to by
        the action being reported if all potential pre-determined or
        pre-negotiated options were exercised, awardee effort is completed or
        the award is otherwise ended. Administrative actions related to this
        award may continue to occur after this date. This date does not apply to
        procurement indefinite delivery vehicles under which definitive orders
        may be awarded."""
    )
    primary_place_of_performance_state_code: Mapped[Optional[str]] = mapped_column(
        doc="""United States Postal Service (USPS) two-letter abbreviation for
        the state or territory indicating where the predominant performance of
        the award will be accomplished. Identify States, the District of
        Columbia, territories (i.e., American Samoa, Guam, Northern Mariana
        Islands, Puerto Rico, U.S. Virgin Islands) and associated states (i.e.,
        Republic of the Marshall Islands, the Federated States of Micronesia,
        and Palau) by their USPS two-letter abbreviation for the purposes of
        reporting. See https://www.fpds.gov/fpdsng_cms/index.php/en/worksite.html"""
    )
    product_or_service_code: Mapped[Optional[str]] = mapped_column(
        String(6),
        doc="""The code that best identifies the product or service procured.
        Codes are defined in the Product and Service Codes Manual. See
        https://www.acquisition.gov/psc-manual""",
    )
    product_or_service_code_description: Mapped[Optional[str]] = mapped_column(
        doc="""Description tag (by way of the FPDS Atom Feed) that explains the
        meaning of the code provided in the Product or Service Code Field. See
        https://www.acquisition.gov/psc-manual"""
    )
    recipient_zip_4_code: Mapped[Optional[str]] = mapped_column(
        doc="""USPS zoning code associated with the awardee or recipient’s legal
        business address. For domestic recipients only. See https://www.fpds.gov/fpdsng_cms/index.php/en/worksite.html"""
    )
    school_district_local_government: Mapped[Optional[str]] = mapped_column(
        doc="""Characteristic of the entity such as whether the selected entity
        is a School District Local Government or not. It is derived from the SAM
        data element, 'Business Types'. See
        https://www.fpds.gov/fpdsng_cms/index.php/en/worksite.html"""
    )
    state_controlled_institution_of_higher_learning: Mapped[Optional[str]] = (
        mapped_column(
            doc="""Characteristic of the entity such as whether the selected entity
        is a State Controlled Institution of Higher Learning or not. It is
        derived from the SAM data element, 'Business Types'. See 
        https://www.fpds.gov/fpdsng_cms/index.php/en/worksite.html"""
        )
    )
    township_local_government: Mapped[Optional[str]] = mapped_column(
        doc="""Characteristic of the entity such as whether the selected entity
        is a Township Local Government or not. It is
        derived from the SAM data element, 'Business Types'. See 
        https://www.fpds.gov/fpdsng_cms/index.php/en/worksite.html"""
    )
    us_local_government: Mapped[Optional[str]] = mapped_column(
        doc="""Characteristic of the entity such as whether the selected entity
        is a Local Government Organization or not. It is
        derived from the SAM data element, 'Business Types'. See 
        https://www.fpds.gov/fpdsng_cms/index.php/en/worksite.html"""
    )
    us_state_government: Mapped[Optional[str]] = mapped_column(
        doc="""Characteristic of the entity such as whether the selected entity
        is a State Government Organization or not. It is
        derived from the SAM data element, 'Business Types'. See 
        https://www.fpds.gov/fpdsng_cms/index.php/en/worksite.html"""
    )
    us_tribal_government: Mapped[Optional[str]] = mapped_column(
        doc="""Characteristic of the entity such as whether the selected entity
        is a Tribal Government Organization or not. It is
        derived from the SAM data element, 'Business Types'. See 
        https://www.fpds.gov/fpdsng_cms/index.php/en/worksite.html"""
    )


class AssistanceTransactionsMixin:
    assistance_award_unique_key: Mapped[Optional[str]] = mapped_column(
        doc="""Unique key of assistance Prime Award Summary. Derived unique
        record key used by the Broker to identify the prime award. Note that
        this element is different from the AssistanceTransactionUniqueKey in
        that it identifies the award, not a specific transaction within the
        award. A concatenation of FAIN, URI, and AwardingSubTierAgencyCode. A
        single underscore ('_') character is inserted in between each element
        value. If an element value is blank then the values used is "NONE"."""
    )
    assistance_transaction_unique_key: Mapped[Optional[str]] = mapped_column(
        doc="""System-generated database key used to uniquely identify each
        financial assistance transaction record and facilitate record lookup,
        correction, and deletion. A concatenation of AwardingSubTierAgencyCode,
        FAIN, URI, CFDA_Number, and AwardModificationAmendmentNumber with a
        single underscore ('_') character inserted in between each. If a field
        is blank, it is recorded as "-none-"."""
    )
    assistance_type_code: Mapped[Optional[str]] = mapped_column(
        String(2), doc="""The type of assistance provided by the award."""
    )
    assistance_type_description: Mapped[Optional[str]] = mapped_column(
        doc="""Description tag (by way of the DATA Act Broker) that explains the
        meaning of the code provided in the AssistanceType Field. See
        https://www.usaspending.gov/data-dictionary"""
    )
    business_types_code: Mapped[Optional[str]] = mapped_column(
        doc="""A collection of indicators of different types of recipients based
        on socio-economic status and organization / business areas. See 
        https://www.usaspending.gov/data-dictionary"""
    )
    business_types_description: Mapped[Optional[str]] = mapped_column(
        doc="""Description tag (by way of the DATA Act Broker) that explains the
        meaning of the code provided in the BusinessType Field."""
    )
    cfda_number: Mapped[Optional[str]] = mapped_column(
        String(6),
        doc="""The number assigned to an Assistance Listing in SAM.gov. See
        <https://sam.gov/content/assistance-listings>""",
    )
    cfda_title: Mapped[Optional[str]] = mapped_column(
        doc="""The title of the Assistance Listing under which the Federal award
        was funded in the Catalog of Federal Domestic Assistance (CFDA) and
        SAM.gov. See https://sam.gov/content/assistance-listings"""
    )
    funding_opportunity_number: Mapped[Optional[str]] = mapped_column(
        doc="""An alphanumeric identifier that a Federal agency assigns to its
        funding opportunity announcement as part of the Notice of Funding
        Opportunity posted on the OMB-designated government wide web site
        (currently grants.gov) for finding and applying for Federal financial
        assistance. See https://grants.gov/search-grants"""
    )
    original_loan_subsidy_cost: Mapped[Optional[float]] = mapped_column(
        doc="""The estimated long-term cost to the Government of a direct loan
        or loan guarantee, or modification thereof, calculated on a net present
        value basis, excluding administrative costs."""
    )
    primary_place_of_performance_code: Mapped[Optional[str]] = mapped_column(
        doc="""A numeric code indicating where the predominant performance of
        the award will be accomplished. See
        https://www.usaspending.gov/data-dictionary"""
    )
    primary_place_of_performance_foreign_location: Mapped[Optional[str]] = (
        mapped_column(
            doc="""For foreign places of performance: identify where the predominant
        performance of the award will be accomplished, describing it as
        specifically as possible."""
        )
    )
    primary_place_of_performance_scope: Mapped[Optional[str]] = mapped_column(
        doc="""A description of the geographic area to which the predominant
        performance of the award is applicable. See
        https://www.usaspending.gov/data-dictionary"""
    )
    recipient_city_code: Mapped[Optional[str]] = mapped_column(
        doc="""Five position city code from the validation authoritative list in
        which the awardee or recipient's legal business address is located See
        https://www.usgs.gov/core-science-systems/ngp/board-on-geographic-names/download-gnis-data"""
    )
    recipient_foreign_city_name: Mapped[Optional[str]] = mapped_column(
        doc="""For foreign recipients only: name of the city in which the
        awardee or recipient's legal business address is located."""
    )
    recipient_foreign_postal_code: Mapped[Optional[str]] = mapped_column(
        doc="""For foreign recipients only: foreign postal code in which the
        awardee or recipient's legal business address is located."""
    )
    recipient_foreign_province_name: Mapped[Optional[str]] = mapped_column(
        doc="""For foreign recipients only: name of the state or province in
        which the awardee or recipient’s legal business address is located."""
    )
    recipient_zip_code: Mapped[Optional[str]] = mapped_column(
        doc="""USPS five digit zoning code associated with the awardee or
        recipient's legal business address. This field must be blank for non-US
        addresses."""
    )
    recipient_zip_last_4_code: Mapped[Optional[str]] = mapped_column(
        doc="""USPS four digit extension code associated with the awardee or
        recipient's legal business address. This must be blank for non-US
        addresses"""
    )


class TransactionDerivationsMixin:
    generated_pragmatic_obligations: Mapped[Optional[float]] = mapped_column(
        doc="""Most commonly used prime award transaction federal spending
        amount. federal_action_obligation for non-loans.
        original_loan_subsity_cost for loans (assistance_type = '07', '08')"""
    )
    action_date_year_month: Mapped[Optional[str]] = mapped_column(
        doc="""'YYYY-MM' from `action_date`"""
    )
    action_date_year: Mapped[Optional[int]] = mapped_column(
        doc="""Year of `transaction.action_date`"""
    )
    award_summary_unique_key: Mapped[Optional[str]] = mapped_column(
        doc="""Uniquely identifies a procurement or assistance prime award
        summary."""
    )


class AssistanceTransactions(
    Base,
    TransactionsMixin,
    AssistanceTransactionsMixin,
    HasId,
    TransactionDerivationsMixin,  # must be inhereted last
):
    __tablename__ = "assistance_transactions"


class ProcurementTransactions(
    Base,
    TransactionsMixin,
    ProcurementTransactionsMixin,
    HasId,
    TransactionDerivationsMixin,  # must be inhereted last
):
    __tablename__ = "procurement_transactions"


class Transactions(
    Base,
    TransactionsMixin,
    TransactionDerivationsMixin,
    ProcurementTransactionsMixin,
    AssistanceTransactionsMixin,
    HasId,
):
    __tablename__ = "transactions"
