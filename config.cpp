#include "script_component.hpp"

class CfgPatches {
    class ADDON {
        author = AUTHOR;
        authors[] = {
            "Cannon",
            "Bragg",
            "Vdoh",
            "Ks00908"
        };
        name = COMPONENT_NAME;
        requiredVersion = REQUIRED_VERSION;
        requiredAddons[] = {
            "ls_main"
        };
        units[] = { };
        weapons[] = { };
        VERSION_CONFIG;
    };
};
