# Parsed Document: /app/tests/fixtures/arxiv-1410.6579.pdf

## Header

1410.6579v1 [quant-ph] 24 Oct 2014

e e

arXiv

Feedback Policies for Measurement-based Quantum State Manipulation

Shuangshuang Fu

College of Engineering and Computer Science The Australian National University, Canberra, Australia

E-mail: shuangshuang.fu@anu. edu. au

Guodong Shi

College of Engineering and Computer Science The Australian National University, Canberra, Australia

E-mail: guodong.shi@anu.edu.au

Alexandre Proutiere

School of Electrical Engineering Royal Institute of Technology, Stockholm, Sweden

E-mail: alepro@kth.se

Matthew R. James

College of Engineering and Computer Science The Australian National University, Canberra, Australia

E-mail: matthew. james@anu. edu. au

Abstract. In this paper, we propose feedback designs for manipulating a quantum state to a target state by performing sequential measurements. In light of Belavkin’s quantum feedback control theory, for a given set of (projective or non-projective) measurements and a given time horizon, we show that finding the measurement selection policy that maximizes the probability of successful state manipulation is an optimal control problem for a controlled Markovian process. The optimal policy is Markovian and can be solved by dynamical programming. Numerical examples indicate that making use of feedback information significantly improves the success probability compared to classical scheme without taking feedback. We also consider other objective functionals including maximizing the expected fidelity to the target state as well as minimizing the expected arrival time. The connections and differences among these objectives are also discussed.

PACS numbers: 03.67.Ac

Keywords: Feedback Policy, Quantum State-manipulation, Quantum Measurement

Feedback Policies for Measurement-based Quantum State Manipulation 2

## 1. Introduction

One fundamental difference between classical and quantum mechanics is the unavoidable back-action of quantum measurement. On the one hand, this back-action is generally thought to be detrimental for the implementation of effective quantum control. On the other hand, it also provides us one possibility to use the change caused by the measurement as a new route to manipulate the state of the system[1, 9]. A basic problem in quantum physics and engineering is how to drive a quantum system to a desired target state. There have been studies on the preparation of a given target state from a given initial state using sequential (projective or non-projective) measurements in the last few years [13, 14, 15, 16, 17]. A quantum measurement F is described by a collection of measurement operators

{Me(m)}

where JY is an index set for measurement outcomes and the measurement operators

YS Meg(m)'Mp(m) = I.

mey

satisfy

Suppose we perform the quantum measurement FE on density operator p, the probability of obtaining result m € Y is tr(Mg(m)pMz(m)'), and when m € Y occurs, the post- measurement state of the quantum system becomes

Mn(m)pMe(m)" tr(Mz(m)pMz(m)*) ”

If we are unaware of the measurement result, the unconditional state of the quantum

Mi (p) =

system after the measurement can be expressed as

=S Ma(m )pMa( m)".

mey

If {Mz(m)}mey are orthogonal projectors, i.e, the Mg(m) are Hermitian and Me(l)Mp(m) = dmMen(m), E is a projective measurement. The idea of quantum state manipulation using sequential measurements [13, 14, 15, 16, 17] is as follows. By consecutively performing the measurements F,..., Ey, the unconditional state for quantum system with initial state po can be expressed as

py = Mey ° Mey_; Or770 Mr, (po):

It has been shown, analytically or numerically, how to select the measurements E\,...,Ey so that p’ can asymptotically tend to a desired target state [13, 14, 15, 16, 17]. Making use of feedback information for quantum measurement and detection actually has a long history, which can be viewed as the dual problem of state

Feedback Policies for Measurement-based Quantum State Manipulation 3

manipulation. The “Dolinar’s receiver” proposes a feedback strategy for discriminating two possible quantum states with prior distribution with minimum probability of error [4]. The problem is known as the quantum detection problem and Helstrom’s bound characterizes the minimum probability of error for discriminating any two non-orthonormal states [6]. Quantum detection is to identify uncertain quantum states via projective measurements; while the considered quantum state projection is to manipulate a certain quantum state to a certain target, again via projective measurements. The Dolinar’s scheme follows a similar structure that measurement is selected based on previous measurement results on different segments of the pulse, and was recently realized experimentally [5]. See [8] for a survey for the extensive studies in feedback (adaptive) design in quantum tomography. In this paper, we propose a feedback design for quantum state manipulation via sequential measurements. For a given set of measurements and a given time horizon, we show that finding the policy of measurement selections that maximizes the probability of successful state manipulation can be solved by dynamical programming. Such derivation of the optimal policy falls to Belavkin’s quantum feedback theory [1]. Numerical examples are given which indicate that the proposed feedback policy significantly improves the success probability compared to classical policy by consecutive projections without taking feedback. In particular, the probability of reaching the target state |1) via feedback policy reaches 0.9968 using merely 10 measurements from initial state |0). Other optimality criteria are also discussed such as the maximal expected fidelity and the minimal arrival time, and some connections and differences among the the different criteria are also discussed. The remainder of the paper is organised as follows. In the first part of Section 2, we revisit a simple example of reaching |1) from |0) using sequential projective measurements [17], and show how feedback policies work under which even a little bit of feedback can make a nontrivial improvement. The rest of Section 2 devotes to a rigorous treatment for the problem definition and for finding the optimal feedback policy from classical quantum feedback theory. Numerical examples are given there. Section 3 investigates some other optimality criteria and finally Section 4 concludes the

paper. 2. Quantum State Manipulation by Feedback

2.1. A Simple Example: Why Feedback?

Consider now a qubit system, i.e., a two-dimensional Hilbert space. The initial state of the quantum system is |0)(0|, and the target state is |1)(1|. Given T > 2 projective measurements from the set

e={ki, i=1,2,...,7h. (1)

Feedback Policies for Measurement-based Quantum State Manipulation 4

where E; = {|:) (|, i) (Wal } with |¢;) = cos (=) 0) + sin (=) 1)

li) = —sin (=) |0) + cos (=) |1).

Note that the choice of E; follows the optimal selection given in [17].

and

The strategy in [16, 17] is simply to perform the T measurements in turn from E, to Er. We call it a naive policy. The probability of successfully driving the state from |0) to |1) in 7 steps under this naive strategy is denoted by p(7’). We can easily calculate that p(3) + 0.56 and p(10) = 0.8. Let T’ = 3. We next show that even only a bit of measurement feedback can improve the performance of the strategy significantly. S1. After the first measurement FE, has been made, perform E3 if the outcome is |) for the second step, and follow the naive policy for all other actions. Following this scheme, it turns out that the probability of arriving at |1) in three steps becomes around 0.66, in contrast with p(3) * 0.56 under the naive scheme. The improvement in the probability of success comes from the fact that a feedback decision is made based on the information of the outcome of E) so that in $1 a better selection of measurement is obtained between FE, and £3.

2.2. Optimal Policy from Quantum Feedback Control

We now present the solution to the optimal policy for the considered quantum state manipulation in light of the classical work of quantum feedback control theory derived by Belavkin [1] (also see [2] and [3] for a thorough treatment). Consider a quantum system whose state is described by density operators over the qubit space. Let € be a given finite set of measurements serving as all feasible control actions. For each EF € €, we write

B= {Mely)}

>] yey

where J is a finite index set of measurement outputs and Mzg(y) is the measurement operator corresponding to outcome y € Y. Time is slotted with a horizon N > 1. The initial state of the quantum system is po, and the target state is assumed to be, for the ease of presentation, |1)(1]. For 0 < k < N —1, we denote by uz € E the measurement performed at time k and the post-measurement state after uz has been performed is denoted as Proi- Let yx € VY be the outcome of uz. The measurement sequence {ur ti is selected by a policy 7 = {tr}e os where each 7, takes value in the set € such that Up = Tr(Yo,--->Yk—1; Uo,---;Uk—-1) can depend on all previous selected measurements and their outcomes for all k = 0,...,N—1. Here for convenience we have denoted

U-1 = Y-1 = 0.

Feedback Policies for Measurement-based Quantum State Manipulation 5

We can now express the closed-loop evolution of {p;,})’ as Mu, (Ye) erMi, (ye) tr (Mu, (yx) Pr Mi, (ys))

where k = 0,..., N —1. The distribution of y, is given by

Pro = Mik (pe) =

P(u =ye Yue, pr.) = tr(M,(y)pxMl,, (y)),

where k = 0,..., N —1. Clearly {p,})" defines a Markov chain. We definet

J(N) = P(oy =[1)(1))

as the probability of successfully manipulating the quantum state to the target density matrix |1)(1|, where P, is the probability measure equipped with 7. We also define the cost-to-go function

V(t,x2) = max P(py = 11) (I os = x)

fort = 0,1,...,.N. Following standard theories for controlled Markovian process [12, 10], the following conclusion holds.

Proposition 1 The cost-to-go function V(t, x) satisfies the following recursion

V(t,2) = max P(ylu,«) V(t — LMY(x)), (3)

ucé yey

wheret =1,...,N, with boundary condition V(0,x) = 1 if x = |1)(1|, and V(0, x) = 0 otherwise. The maximum arrival probability max, J,(N) is given by max, J,(N) = V(N, po). The optimal policy 1 = {ri} n ot is Markovian, and is given by

7}, (Pk) = arg max) P(y u, pr) V(N —k— 1, Mi(o%)) (4) yey

fork =0,...,N—1.

2.8. Numerical Examples

We now compare the performance of the policies with and without feedback. Again we consider driving a two-level quantum system from state |0) to |1). The available measurements are in the set

é={ki, i=1,2,...,T}.

as given in Eq.(1).

t It is clear from this objective that E, = {|0)(0|,|1)(1|} must be a measurement in the set € for J,(N) to be a non-trivial function if all measurements in € are projective.

Feedback Policies for Measurement-based Quantum State Manipulation 6

100 : : : : : _—

J» (N) and J+ (N)

Figure 1. The probabilities of successfully reaching |1) from the initial state |0) using naive policy 7" and optimal feedback policy 7*, respectively.

2.8.1. Feedback vs. Non-Feedback First of all, we take T = N. The naive policy in turn takes projections from E, to Ey, denoted 1” = {ar We solve the optimal feedback policy 1* = {mx} o' using Eq. (4). It is clear that 7 is deterministic with Te = Exyi, while 7 is Markovian with 7 depending on pz. Correspondingly, their arrival probability in N steps are given by J,n(N) and J,«(V), respectively. In Figure 1, we plot J,zn(N) and J,«(NV) for N = 3,...,10. As shown clearly in the figure, the probability of success is improved significantly. Actually for N = 10, we already have J+(N) = 0.9968. Moreover, as an illustration of the different actions between the naive and feedback strategies, we plot their policies for N = 5 in Tables I and II, respectively.

2.8.2. Influence of Measurement Set We now investigate how the size of the available measurement set € influences the successful arrival probability in N steps under optimal feedback. In this case, the optimal arrival probability J,.«(NV) is also a function of T, and we therefore rewrite J,«(N) = JZ.(N). In Figure 2, we plot J7.(N), for T = 10,100, 1000, respectively. The numerical results show that as T increases, the J“, (N) quickly tends to a limiting curve, suggesting the existence of some fundamental upper bound on the arrival probability in N steps using sequential projections from an arbitrarily large measurement set.

3. More Optimality Criteria

In this section, we discuss two other useful optimality criteria, to maximize the expected fidelity with the target state, or to minimize the expected time it takes to arrive at the

Feedback Policies for Measurement-based Quantum State Manipulation 7

m™ |kK=O)/k=1)/k=2)k=3|\/k=4 |0) Ey * * a. |1) x x * * * 1) * Ey * * * w1) * Ey * * * 2) x x E3 x x we) x x E3 x x 3) x x x Ey x ws) x x x Ey x 4) x x x x Es wa) x x x x Es

Table 1. The actions using naive strategy 7" to prepare the target state |1), starting from |0), for N = 5. Here E; represents the measurement that the policy chooses, and * means that it is not possible to be in that state at the corresponding step.

m™ |k=O0|k=1|/k=2|k=3/k=4 )_ & | & | & | & | 1) | Es | Bs | Bs | Es | Es

SSESEREE & & & & &

Table 2. The actions using optimal feedback policy z* to prepare the target state |1) for N =5.

target state.

3.1. Maximal Expected Fidelity

Given two density operators p and o, their fidelity is defined by [7|

F(p,o) = try//pov/p.

Feedback Policies for Measurement-based Quantum State Manipulation 8

(N)

T Jos

1 1 1 \ nl n 3 4 5 6 7 a 9 10

Steps N Figure 2. The probabilities of successfully reaching |1) from the initial state |0) using

different sizes of measurement set by feedback strategy.

Fidelity measures the closeness of two quantum states. Now that our target state |1)(1| is a pure state, we have

try VID Alo Vy] = Vor).

Alternatively, we can consider the following objective functional

Jn(N) = Ex (1/0, 1)],

and the goal is to find a policy that maximizes J Jn(N ). For the two objective functionals Jn (N) and J,(N), we denote their corresponding optimal policy as m*(N) = {77(N)}7! and 7°(N) = {r2(N)}\ 3, respectively, where the time horizon N is also indicated, Let 7°(N —1)@ E, be the policy that follows t°(N —1) for k =0,...,N—2 and takes value EF, for k = N — 1. Let p? be the unconditional density operator at step k fork =0,...,N—1. The following equations hold:

Jo(N = 1) =E,|(Hpy-11)| tr(p%_,J1)(LI) = Px (oy =[1)(1\), (5)

for any 7 = {tr}po where 7’ = 70 E, = {te} po. with tmy_; = E,. As a result, the following relation holds between the optimal policies under the two objectives J,(NV) and J,(N).

Feedback Policies for Measurement-based Quantum State Manipulation 9

Proposition 2 /t holds that max,J,(N) = max, Jy (VN —1). In fact, m*(N) = n°(N —1) @ E, with E, = {|0) (0, 1) (13.

The intuition behind Proposition 2 is that one would expect to get as closely as possible to the target state at step N — 1, if one tends to successfully project onto the target state at step N. We also know from Proposition 2 that we can solve the maximal expected fidelity problem in N steps by the solutions of maximizing the arrival probability in N +1 steps. Similarly, we can also find the optimal policy 7° for the objective J,(N) using dynamical programming. Define the cost-to-go function V(k,x) for J,(N) as

V(k, ©) = maxE,|(1|py|1) | px = 2| (6) fork =0,...,N. Then V(k, x) satisfies the following recursive equation \/ _ \/ y V(k, 2) = max )>P(y|ue)V (kK +1.MY(2)), (7) yey for k =0,...,N —1, with terminal condition V(N, a) = tr(x]1) (1). (8)

The optimal policy 7° can be obtained by solving

Te (pe) = arg max )>P(y U, pe) (K + L,M4(o%)) yey

for k =0,...,N —1. The maximal expected fidelity J,o(N) = V(0, po).

3.2. Minimal Arrival Time

In previous discussions the deadline N plays an important role in the objective functionals as well as in their solutions. We now consider the case when the deadline is flexible, and we aim to minimize the average number of steps it takes to arrive at the target state. Now the control policy is denoted as 7 = {7,}?25, where 7% selects a measurement from the set €. Associated with 7, we define

of, = int { py = [1)(U} (9)

Note that <% defines a stopping time (cf., [11]) associated with the random processes {px}o°, and we assume that 7 is proper in the sense that

Ps (% <0) =1.

We continue to introduce

J, = Ex[ Ar] (10)

as the objective functional, which is the expected time it takes for the quantum state

to reach the target |1)(1| following policy 7. Minimizing J’. is a stochastic shortest path problem [18].

Feedback Policies for Measurement-based Quantum State Manipulation 10

x | |0) | |1) | lr) | [ea | 12) | Pb2) | los) | tees) | Iba) ] Iara) ia (x) E» Es Es Es Ey Es Es EF, Es E»

Table 3. The optimal policy 74 minimizing the expected time it takes for the quantum state to reach the target state |1)(1| for control set €, with T = 5.

We introduce &,(x) := inf, {px = |1)(1| | po = x} and V’(x) = minE, Ez0) (11)

TT

The Markovian property of {pz }% leads to that the optimal policy 74 is stationary in the sense that 7, = 7'(x) for all k. The following conclusion holds applying directly the results of [18].

Proposition 3 The cost-to-go function V’ satisfies the following recursion

W(x) =1+4+ mip Pol r)V (Mi(2)), (12)

for all x« 4 |1)(1|, with boundary condition V?(\1)(1|) = 0. The optimal policy 7° is given by

n(x) = arg min Ye P(y U, x)V (Mi(x)). (13) yey

The optimal J’, is given by J, = V" (po):

Technically it cannot be guaranteed that for any given measurement set €, there always exists at least one policy 7 under which J’. admits a finite number. However, some straightforward calculations indicate that for the set € of projective measurements given in Eq. (1), finite J’. can always be achieved for a class of policies.

3.8. Numerical Example: Minimal Arrival Time

Again, consider T projective measurements from the set [17] E= {E, i= 12.2.7},

In Figure 3, we plot J, (T) as a function of T, for T = 2,3,...,30. Numerical calculations show that the minimized average number of steps of driving |0)(0] to |1)(1| does not depend too much on the size of control set, it oscillates around 3.8 for control sets of reasonable size. Also for measurement set €, with T’ = 5, we show the optimal policy 7° in Table 3.

Feedback Policies for Measurement-based Quantum State Manipulation 11

Minimal Arrival Time

3.90

3.85

3.60

375 nl n 1 n nl 0 5 10 15 20 3 30

Size T

Figure 3. The minimized average number of steps it takes to arrive at the target state |1)(1| from the initial state |0)(0| employing control set €, of size T.

4. Conclusions

We have proposed feedback designs for manipulating a quantum state to a target state by performing sequential measurements. Making use of Belavkin’s quantum feedback control theory, we showed that finding the measurement selection policy that maximizes the probability of successful state manipulation is an optimal control problem which can be solved by dynamical programming for any given set of measurements and a given time horizon. Numerical examples indicate that making use of feedback information significantly improves the success probability compared to classical scheme without taking feedback. It was shown that the probability of reaching the target state via feedback policy reaches 0.9968 using merely 10 steps, while classical results [16, 17] suggested that naive strategy via consecutive measurements in turn reaches success probability one when the number of steps tends to infinity. Maximizing the expected fidelity to the target state and minimizing the expected arrival time were also considered, and some connections and differences among these objectives were also discussed.

Acknowledgments We gratefully acknowledge support by the Australian Research Council Centre of Excellence for Quantum Computation and Communication Technology (project number CE110001027), and AFOSR Grant FA2386-12-1-4075).

## References

[1] V. P. Belavkin, Towards control theory of quantum observable systems, Automatica and Remote Control, vol. 44, $188, 1983.

Feedback Policies for Measurement-based Quantum State Manipulation 12

2

am

10

11

12

13

14

15

16

17

18

M. R. James, Risk-sensitive optimal control of quantum systems, Physical Review A, vol. 69, 032108, 2004. L. Bouten, R. Van Handel, and M. R. James, A discrete invitation to quantum filtering and feedback control, STAM Review, 51(2), 239-316, 2009. S. J. Dolinar, An optimum receiver for the binary coherent state quantum channel, MIT Res. Lab. Electron. Quart. Progr. Rep., 111, pp. 115-120, 1973. R. L. Cook, P. J. Martin, and J. M. Geremia, An optimum receiver for the binary coherent state quantum channel, Nature, vol. 446, pp.774-777, 2007. C. W. Helstrom. Quantum Detection and Estimation Theory. Academic press, 1976. M. A. Nielsen and I. L. Chuang. Quantum Computation and Quantum Information. Cambridge university press. 2010. H. M. Wiseman, D. W. Berry, S. D. Bartlett, B. L. Higgins, and G. J. Pryde, Adaptive measurements in the optical quantum information laboratory, IEEE Journal of Selected Topics in Quantum Electronics, vol. 15, no. 6, pp. 1661-1672, 2009. H. M. Wiseman and G. J. Milburn, Quantum theory of optical feedback via homodyne detection, Physical Review Letters, vol. 70, no. 5, 548, 1993. M. L. Puterman. Markov Decision Processes: Discrete Stochastic Dynamic Programming. New York : Wiley, 1994. R. Durrett. Probability: Theory and Examples, Duxbury advanced series, Third Edition, Thomson Brooks/Cole, 2005. D. P. Bertsekas. Dynamic Programming and Optimal Control. Vol. Il, 4th Edition. Athena Scientific, 2012. S. Ashhab and F. Nori, Control-free control: manipulating a quantum system using only a limited set of measurements, Physical Review A, 82(6), 062103, 2010. K. Jacobs, Feedback control using only quantum back-action, New Journal of Physics, 12(4), 043005, 2010. H. M. Wiseman, Quantum control: Squinting at quantum systems, Nature, vol. 470, no. 7333, pp. 178-179, 2011. L. Roa, M. L. de Guevara, A. Delgado, G. Olivares-Renteria, and A. Klimov, Quantum evolution by discrete measurements, Journal of Physics: Conference Series, vol. 84, 012017, 2007. A. Pechen, N. IVin, F. Shuang, and H. Rabitz, Quantum control by von neumann measurements, Physical Review A, vol. 74, no. 5, p. 052102, 2006. D. P. Bertsekas and J. N. Tsitsiklis, An analysis of stochastic shortest path problems, Mathematics of Operations Research, 16(3), pp. 580-595, 1991.
