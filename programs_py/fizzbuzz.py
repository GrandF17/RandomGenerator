from seahorse.prelude import *

# This is your program's public key and it will update
# automatically when you build the project.
declare_id('gDWobBFabkrhT8YwKRQi1ktx6oZCvyzKm87KBZ7nScr')

# linear congruent method of generating
# pseudo-random numbers
# X_n = (a * X_(n-1) + c) mod( m ) 
# seed_0 = timestamp, seed_1 = f(seed_0), seed_2 = f(seed_1), ...
class Random:
  a: u64
  c: u64
  m: u64
  next: u64

  # a and c values where borrowed according to 
  # Donald Khnut researches
  def __init__(self, seed: u64):
    self.a = 6_364_136_223_846_793_005 
    self.c = 1_442_695_040_888_963_407
    self.m = 18_446_744_073_709_551_615 # max value can be stored in u64 type
    self.next = seed                    # could be time or another source of entropy

  def rand(self):
    self.next = u64((self.next * self.a + self.c) % self.m)

class Generator(Account):
  owner: Pubkey
  state: Random


@instruction
def init(owner: Signer, gen: Empty[Generator], clock: Clock):
  _gen = gen.init(
    payer=owner, 
    seeds=['Generator', owner],
  )
  _gen.owner = owner.key()
  _gen.state = Random(u64(clock.unix_timestamp()))

  print("Your personal generator created: ", _gen.key())


@instruction
def rand(caller: Signer, gen: Generator):
  assert caller.key() == gen.owner, "You are not the owner, filthy motherfucker!"
  
  gen.state.rand()
  print("New random number generated: ", gen.state.next)


@instruction
def relinquish_ownership(caller: Signer, gen: Generator, newOwner: Pubkey):
  assert caller.key() == gen.owner, "Only owner can set new owner!"
  
  gen.owner = newOwner
  print("Owner switched to: ", gen.owner)