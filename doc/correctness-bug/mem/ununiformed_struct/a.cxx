#include <iostream>
#pragma pack(push, 8)
#include "hdr.h"
#pragma pack(pop)

void func(S* s);

int main() {
    S* s = new S {};
    func(s);
    std::cout << "a.cxx: " << sizeof (S) << std::endl;
    std::cout << "a.cxx: " << "filed-a:" << s->a << " filed-b:" << s->b << " filed-c:" << s->c << std::endl;
    return 0;
}
