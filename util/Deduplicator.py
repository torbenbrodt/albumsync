class Deduplicator:

    def __init__(self):
        pass

    def run_list(self, ll, callback_init, callback_id):
        sort_dict = {}
        match_dict = {}
        for web_ref in ll:
            keyid = callback_id(web_ref)
            media = callback_init(web_ref)
            sort_dict[keyid] = media
            if media.get_match_name() in match_dict:
                match_dict[media.get_match_name()] += 1
            else:
                match_dict[media.get_match_name()] = 1

        for keyid in sorted(sort_dict.iterkeys()):
            media = sort_dict[keyid]
            # first hit, will not rename, but it will set the -1
            if match_dict[media.get_match_name()] > 1:
                match_dict[media.get_match_name()] = -1
            elif match_dict[media.get_match_name()] == -1:
                media.set_title(str(keyid) + '_' + media.get_title())

        return sort_dict.values()