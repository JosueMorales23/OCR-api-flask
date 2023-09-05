import re

document_type_pattern = r'BENEFITS\s*IDENTIFICATION\s*CARD'
id_pattern = r'(IDNo\.|No.)\s*(\w+)'
name_pattern = r'(IDNo\.|No.)\s*(\w+)\s*(\d+)\s*(\w{3,}\s*\w{1,})'
issue_date_pattern = r'(Issue\s*Date|Date)\s*(\d{2}\s*\d{2}\s*\d{2})'

document_type_pattern2 = r'MediCal\s*Program'
member_id_pattern = r'Member\s*ID\s*(\w+)'
name_pattern2 = r'Name\s*((\w{2,})\s*(\w{1,})\s*(\w{2,}))'
effective_date_pattern = r'Effective\s*Date\s*(\d{1}\d{1}\d{4})'

# specifics patterns
pattern_member_id = r'Member\s*ID|ID\s*No|Member'

document_type_pattern3 = r'Benefits'
document_type_pattern4 = r'Identification'
document_type_pattern5 = r'Card'
name_pattern3 = r'ID\s*No\s*(\w+)\s*(\w+)\s*(\w{3,}\s*\w{1,}\s*\w{2,})'
document_type_pattern6 = r'Anthem'
document_type_pattern7 = r'LA Care'
document_type_pattern8 = r'BlueCross'


def search_patterns(text):
    document_type_match = re.search(document_type_pattern, text, re.IGNORECASE)  # match 0
    id_match = re.search(id_pattern, text, re.IGNORECASE)  # match 1
    name_match = re.search(name_pattern, text, re.IGNORECASE)  # match 2
    issue_date_match = re.search(issue_date_pattern, text, re.IGNORECASE)  # match 3

    document_type_match2 = re.search(document_type_pattern2, text, re.IGNORECASE)  # match 4
    member_id_match = re.search(member_id_pattern, text, re.IGNORECASE)  # match 5
    name_match3 = re.search(name_pattern2, text, re.IGNORECASE)  # match 6
    effective_date_match = re.search(effective_date_pattern, text, re.IGNORECASE)  # match 7

    # specifics patterns
    pattern_member_id_match = re.search(pattern_member_id, text, re.IGNORECASE)  # match 8

    document_type_pattern3_match = re.search(document_type_pattern3, text, re.IGNORECASE)  # match 9
    document_type_pattern4_match = re.search(document_type_pattern4, text, re.IGNORECASE)  # match 10
    document_type_pattern5_match = re.search(document_type_pattern5, text, re.IGNORECASE)  # match 11
    name_pattern3_match = re.search(name_pattern3, text, re.IGNORECASE)  # match 12
    document_type_pattern6_match = re.search(document_type_pattern6, text, re.IGNORECASE)  # match 13
    document_type_pattern7_match = re.search(document_type_pattern7, text, re.IGNORECASE)  # match 14
    document_type_pattern8_match = re.search(document_type_pattern8, text, re.IGNORECASE)  # match 15

    return (
        document_type_match, id_match, name_match, issue_date_match,
        document_type_match2, member_id_match, name_match3, effective_date_match,
        pattern_member_id_match, document_type_pattern3_match, document_type_pattern4_match,
        document_type_pattern5_match, name_pattern3_match, document_type_pattern6_match,
        document_type_pattern7_match, document_type_pattern8_match
    )
