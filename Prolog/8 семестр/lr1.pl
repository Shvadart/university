:- working_directory(_, 'C:/users/artem/documents/prolog').

:- dynamic is_ans/2.
:- dynamic ��������/1.
:- dynamic answer/2.

:- multifile ����_����������������/1.
:- multifile �������_�����/1.
:- multifile ����_������/1.
:- multifile ������_������/1.
:- multifile ��/1.
:- multifile prove/3.
:- multifile ask_ans/2.
:- multifile ans_check/2.
:- multifile askable/1.
:- multifile option_list/2.
:- multifile update_option/2.
:- multifile update_option_if_new/2.
:- multifile ensure_expected/4.
:- multifile ask_attribute/2.
:- multifile print_options/2.
:- multifile my_asserta/1.
:- multifile story/0.
:- multifile conj/2.
:- multifile wrap/3.
:- multifile read_languages/1.
:- multifile read_languages_aux/2.
:- multifile add_candidate/0.
:- multifile build_clause_body/6.
:- multifile write_candidate_to_file/6.
:- multifile write_list_lines/3.
:- multifile clear_history/0.
:- multifile run_expert/0.
:- multifile menu/0.
:- multifile candidate_menu/0.

:- op(500, xfy, <==).
:- op(500, xfy, /).

% ��������� askable-��������� ��� ������������
:- dynamic ����_����������������/1.
:- dynamic �������_�����/1.
:- dynamic ����_������/1.
:- dynamic ������_������/1.
:- dynamic ��/1.

% ��������� ����������� ����������� ��� ���� ����������
:- discontiguous ����_����������������/1.
:- discontiguous �������_�����/1.
:- discontiguous ����_������/1.
:- discontiguous ������_������/1.
:- discontiguous ��/1.

% "��������" ��� askable-����������, ����� ��� ������������ � �� �������� ������
����_����������������(_) :- fail.
�������_�����(_) :- fail.
����_������(_) :- fail.
������_������(_) :- fail.
��(_) :- fail.

% �������� ���� ������ ���������� � ���� ����� �� ��������� ������
:- consult('candidates.pl').
:- consult('options_db.pl').

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% �������� ���������� � ��������������
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

prove(G, G, _) :-
    predicate_property(G, built_in),
    call(G), !.

prove(G, true, _) :-
    G = true, !.

prove((G, Gs), (P, Ps), Q) :- !,
    prove(G, P, Q),
    prove(Gs, Ps, Q), !.

prove(G, (G <== Ps), Q) :-
    \+ askable(G),
    clause(G, Gs),
    prove(Gs, Ps, [G <== Gs | Q]),
    my_asserta(is_ans(G, true)).

prove(G, G, _) :-
    is_ans(G, false), !, fail.

prove(G, G, _) :-
    is_ans(G, true), !, true.

prove(G, G, Q) :-
    ask_ans(G, Q), !.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% �������� ������� � ���������� ����������� �������
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

ask_ans(G, Q) :-
    askable(G),
    G =.. [Pred, _Expected],
    ( answer(Pred, _) -> true ;
      ask_attribute(G, UserAnswer),
      assertz(answer(Pred, UserAnswer))
    ),
    ans_check(G, Q).

ans_check(G, Q) :-
    G =.. [Pred, Expected],
    answer(Pred, A),
    ( A == ������ ->
         ( Q = [Hypothesis <== Conditions | _] ->
               format("����������� ��������: ~w\n", [Hypothesis]),
               format("��� ��������� �������: ~w\n", [Conditions])
         ; true ),
         retractall(answer(Pred, _)),
         ask_attribute(G, NewAnswer),
         assertz(answer(Pred, NewAnswer)),
         ans_check(G, Q)
    ; A == ��� ->
         short_story,
         retractall(answer(Pred, _)),
         ask_attribute(G, NewAnswer),
         assertz(answer(Pred, NewAnswer)),
         ans_check(G, Q)
    ; A == Expected ->
         true
    ;
         fail
    ).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% ��������� ��� askable-���������
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

askable(t(����_����������������/_)).
askable(t(�������_�����/_)).
askable(t(����_������/_)).
askable(t(������_������/_)).
askable(t(��/_)).

askable(����_����������������(_)).
askable(�������_�����(_)).
askable(����_������(_)).
askable(������_������(_)).
askable(��(_)).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% ��������������� ��������� ��� ����
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

option_list(Attr, Options) :-
    findall(Opt, option(Attr, Opt), Options).

update_option(Attr, Option) :-
    open('options_db.pl', append, Stream),
    format(Stream, 'option(~q, ~q).~n', [Attr, Option]),
    close(Stream).

update_option_if_new(Attr, Value) :-
    ( option(Attr, Value) ->
         true
    ;
         update_option(Attr, Value),
         assertz(option(Attr, Value))
    ).

ensure_expected(Attr, Expected, OptionsTemp, OptionsFinal) :-
    ( member(Expected, OptionsTemp) ->
         OptionsFinal = OptionsTemp
    ;
         update_option_if_new(Attr, Expected),
         OptionsFinal = [Expected|OptionsTemp]
    ).

ask_attribute(G, Answer) :-
    G =.. [Pred, Expected],
    ( option_list(Pred, BaseOptions) -> true ; BaseOptions = [Expected] ),
    OptionsFiltered = BaseOptions,
    ensure_expected(Pred, Expected, OptionsFiltered, OptionsNoWhy),
    append(OptionsNoWhy, [������, ���], Options),
    format("�������� �������� ��� ~w:\n", [Pred]),
    print_options(Options, 1),
    format("��� ����� (������� �����): "),
    read(Choice),
    ( integer(Choice),
      nth1(Choice, Options, Selected) ->
         Answer = Selected
    ; writeln('�������� �����, ���������� �����.'),
      ask_attribute(G, Answer)
    ).

print_options([], _).
print_options([Opt|Rest], N) :-
    format("~w. ~w\n", [N, Opt]),
    N1 is N + 1,
    print_options(Rest, N1).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% ���������� ���������� � ��������������� � �������
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

my_asserta(is_ans(G, V)) :-
    retract(is_ans(G, V)),
    assert(is_ans(G, V)), !.
my_asserta(is_ans(G, V)) :-
    assert(is_ans(G, V)), !.

% ����������� ������ ��������� ��� �������
attributes([����_����������������, �������_�����, ����_������, ������_������, ��]).

% ���������������� �������� story/0 ��� ������ ������� � �������� �������
story :-
    writeln("�������:"),
    attributes(Attrs),
    forall(member(Pred, Attrs),
           ( answer(Pred, A) ->
               findall(Opt, option(Pred, Opt), Options),
               forall(member(Opt, Options),
                      ( (Opt == A -> V = true ; V = false),
                        G =.. [Pred, Opt],
                        format("G = ~w  V = ~w\n", [G, V])
                      )
               )
           ; true  % ���������� ��������, ������� �� ���� ���������
           )
    ).

% �������� ��� ������ ����������� ������� �� ������ ������
short_story :-
    findall(P, (answer(P, A), A \== ������, A \== ���), AskedAttrs),
    list_to_set(AskedAttrs, UniqueAttrs),
    ( UniqueAttrs = [] ->
        writeln("��� ����������� ��������� �� ������ ������.")
    ;
        writeln("����������� ������� �� ������ ������:"),
        forall(member(P, UniqueAttrs),
               ( answer(P, A),
                 option_list(P, Options),
                 forall(member(Opt, Options),
                        ( (Opt == A -> V = true ; V = false),
                          G =.. [P, Opt],
                          format("G = ~w  V = ~w\n", [G, V])
                        )
                 )
               )
        )
    ).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% ��������������� ��������� ��� ������ � �����������
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

conj([], true).
conj([G], G).
conj([G|Gs], (G, Rest)) :-
    conj(Gs, Rest).

wrap(P, Arg, Goal) :-
    Goal =.. [P, Arg].

read_languages(Languages) :-
    write('������� ���� ����������������: '), read(Lang),
    read_languages_aux([Lang], Languages).

read_languages_aux(Acc, Languages) :-
    writeln('�������� ��� ����? (1 - ��, 2 - ������� � ���������� ������)'),
    read(Choice),
    ( Choice = 1 ->
         write('������� ���� ����������������: '), read(NextLang),
         append(Acc, [NextLang], NewAcc),
         read_languages_aux(NewAcc, Languages)
    ; Choice = 2 ->
         Languages = Acc
    ; writeln('�������� �����, �������, ��� ������ ������ �� �����������.'),
         Languages = Acc
    ).

add_candidate :-
    write('������� ��� ��������� (��������, ivan): '), read(Name),
    read_languages(Languages),
    forall(member(Lang, Languages), update_option_if_new(����_����������������, Lang)),
    write('������� ������� ����� (��������, junior, middle, senior): '), read(Level),
    update_option_if_new(�������_�����, Level),
    write('������� ���� ������ (����� ���, ��������, 5): '), read(WorkExp),
    update_option_if_new(����_������, WorkExp),
    write('������� ������ ������ (�������� ��� ����): '), read(WorkFormat),
    update_option_if_new(������_������, WorkFormat),
    write('������� �� (��������, 30000 ��� 50000): '), read(Salary),
    update_option_if_new(��, Salary),
    build_clause_body(Languages, Level, WorkExp, WorkFormat, Salary, Body),
    assertz((��������(Name) :- Body)),
    writeln('����� �������� �������� � ���� ������.'),
    write_candidate_to_file(Name, Languages, Level, WorkExp, WorkFormat, Salary).

build_clause_body(Languages, Level, WorkExp, WorkFormat, Salary, Body) :-
    maplist(wrap(����_����������������), Languages, LanguageGoals),
    conj(LanguageGoals, LanguagesConj),
    wrap(�������_�����, Level, LevelGoal),
    wrap(����_������, WorkExp, WorkExpGoal),
    wrap(������_������, WorkFormat, FormatGoal),
    wrap(��, Salary, SalaryGoal),
    Body = (LanguagesConj, LevelGoal, WorkExpGoal, FormatGoal, SalaryGoal).

write_candidate_to_file(Name, Languages, Level, WorkExp, WorkFormat, Salary) :-
    open('candidates.pl', append, Stream),
    format(Stream, '\n%% ����� ��������\n', []),
    format(Stream, '��������(~w) :-\n', [Name]),
    write_list_lines(Stream, Languages, '����_����������������'),
    format(Stream, '    ~w(~w),\n', ['�������_�����', Level]),
    format(Stream, '    ~w(~w),\n', ['����_������', WorkExp]),
    format(Stream, '    ~w(~w),\n', ['������_������', WorkFormat]),
    format(Stream, '    ~w(~w).\n', ['��', Salary]),
    close(Stream).

write_list_lines(_, [], _).
write_list_lines(Stream, [X], Predicate) :-
    format(Stream, '    ~w(~w),\n', [Predicate, X]).
write_list_lines(Stream, [X|Xs], Predicate) :-
    format(Stream, '    ~w(~w),\n', [Predicate, X]),
    write_list_lines(Stream, Xs, Predicate).

clear_history :-
    retractall(is_ans(_,_)),
    retractall(answer(_,_)).

% ���������������� run_expert � ������� ����� ������
run_expert :-
    clear_history,
    ( prove(������(��������), Proof, [])
      -> ( format("��������� ������� ���������: ~w\n", [��������]),
           writeln("��������������:"),
           writeln(Proof)
         )
      ; writeln('�� ������ ��������, ��������������� ��������.')
    ),
    writeln('1. �������� �������'),
    writeln('2. ����� � ����'),
    read(Choice),
    ( Choice = 1 ->
         story
    ; Choice = 2 ->
         true
    ; writeln('�������� �����, ������������ � ����.')
    ).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% ���� ���������
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

menu :-
    writeln('����:'),
    writeln('1. ������ ������ ���������'),
    writeln('2. ��������� ������ ���������'),
    writeln('3. �����'),
    writeln('�������� ����� (1, 2 ��� 3):'),
    read(Choice),
    ( Choice = 1 ->
         candidate_menu
    ; Choice = 2 ->
         run_expert,
         menu
    ; Choice = 3 ->
         writeln('����� �� ���������.'),
         halt
    ; otherwise ->
         writeln('�������� �����, ���������� �����.'),
         menu
    ).

candidate_menu :-
    add_candidate,
    writeln('�������� ��� ���������? (1 - ��, 2 - ��������� � ������� ����)'),
    read(Choice),
    ( Choice = 1 ->
         candidate_menu
    ; Choice = 2 ->
         menu
    ; writeln('�������� �����, ���������� � ������� ����.'),
         menu
    ).

% ����������� ��������� ������� ���������
������(��������) :-
    ��������(��������).

:- initialization(menu).
