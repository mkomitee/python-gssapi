from flufl.enum import Enum
from flufl.enum import IntEnum
from gssapi.base.ctypes import *
from gssapi.base.status_utils import displayStatus

class NameType(IntEnum):
#   hostbased_service = GSS_C_NT_HOSTBASED_SERVICE 
#   principal = GSS_C_NT_PRINCIPAL_NAME
#   user = GSS_C_NT_USER_NAME
#   anonymous = GSS_C_NT_ANONYMOUS
#   machine_uid = GSS_C_NT_MACHINE_UID_NAME
#   string_uid = GSS_C_NT_STRING_UID_NAME
#   export = GSS_C_NT_EXPORT_NAME
    hostbased_service = 0
    principal = 1
    user = 2
    anonymous = 3
    machine_uid = 4
    string_uid = 5
    export = 6
    # NOTE: there are more kerberos specific names, but I think
    #       those are just hold-overs from before the GSS_C_NT_
    #       names were there (check gss_krb5_nt_)

class RequirementFlag(IntEnum):
    delegate_to_peer = GSS_C_DELEG_FLAG
    mutual_authentication = GSS_C_MUTUAL_FLAG
    replay_detection = GSS_C_REPLAY_FLAG
    out_of_sequence_detection = GSS_C_SEQUENCE_FLAG
    confidentiality = GSS_C_CONF_FLAG
    integrity = GSS_C_INTEG_FLAG
    anonymous = GSS_C_ANON_FLAG
    transferable = GSS_C_TRANS_FLAG

class MechType(IntEnum):
    kerberos = 0

# TODO(ross): make an error for each error return code
class GSSError(Exception):
    def __init__(self, maj_code, min_code):
        self.maj_code = maj_code
        self.min_code = min_code
        
        super(GSSError, self).__init__(self.gen_message())

    def get_all_statuses(self, code, is_maj):
        res = []
        last_str, last_ctx, cont = displayStatus(code, is_maj)
        res.append(last_str)
        while cont:
            last_str, last_ctx, cont = displayStatus(code, is_maj, message_context=last_ctx)
            res.append(last_str)
        
        return res

    def gen_message(self):
        maj_statuses = self.get_all_statuses(self.maj_code, True)
        min_statuses = self.get_all_statuses(self.min_code, False)

        return "Major ({maj_stat}): {maj_str}, Minor ({min_stat}): {min_str}".format(
            maj_stat = self.maj_code,
            maj_str = maj_statuses,
            min_stat = self.min_code,
            min_str = min_statuses
        )
