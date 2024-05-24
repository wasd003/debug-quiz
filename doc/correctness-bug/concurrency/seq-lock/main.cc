#include <unordered_map>
#include <vector>
#include <algorithm>
#include <chrono>
#include <cstdlib>
#include <thread>
#include <atomic>
#include <cstdio>
#include <unistd.h>
#include <sys/types.h>

using namespace std;

typedef struct {
    atomic<int> last_requested; // tid of thread who most recently requested this lock
    atomic<int> last_owner; // tid of thread who most recently acquired this lock
    atomic<int> locked; // flag indicating lock is currently held
} lock_t;

int mutex_init(lock_t* lock) {
    lock->last_requested = -1;
    lock->last_owner = -1;
    lock->locked = 0;
    return 0;
}

void mutex_lock(lock_t* lock) {
    int me = gettid();
    int before_me = atomic_exchange(&(lock->last_requested), me);
    while (lock->last_owner != before_me) {
        continue;
    }
    while (lock->locked) {
        continue;
    }
    lock->locked = 1;
    lock->last_owner = me;
}

void mutex_unlock(lock_t* lock) {
    lock->locked = 0;
}

lock_t lk;
int cnt = 0;

int main() {
    mutex_init(&lk);
    vector<thread> thread_list;
    for (int i = 0; i < 3; i ++ ) {
        thread_list.emplace_back([]() {
            const int tid = gettid();
            for (int j = 0; j < 10000; j ++ ) {
                mutex_lock(&lk);
                cnt ++ ;
                mutex_unlock(&lk);
            }
        });
    }

    for (int i = 0; i < thread_list.size(); i ++ ) thread_list[i].join();
    printf("cnt:%d\n" ,cnt);
    return 0;
}
