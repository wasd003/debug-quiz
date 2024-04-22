#include <iostream>
#pragma pack(push, 4)
#include "hdr.h"
#pragma pack(pop)

void func(S* s) {
    std::cout << "b.cxx: " << sizeof (S) << std::endl;
    s->a = 0xaabb;
    s->b = 0x1122334455667788;
    s->c = 0x11223344;
    std::cout << "b.cxx: " << "filed-a:" << s->a << " filed-b:" << s->b << " filed-c:" << s->c << std::endl;
}
