:- working_directory(_, 'C:/users/artem/documents/prolog').

:- dynamic is_ans/2.
:- dynamic кандидат/1.
:- dynamic answer/2.

:- multifile язык_программирования/1.
:- multifile уровень_опыта/1.
:- multifile опыт_работы/1.
:- multifile формат_работы/1.
:- multifile зп/1.
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

% Объявляем askable-предикаты как динамические
:- dynamic язык_программирования/1.
:- dynamic уровень_опыта/1.
:- dynamic опыт_работы/1.
:- dynamic формат_работы/1.
:- dynamic зп/1.

% Разрешаем разобщённые определения для этих предикатов
:- discontiguous язык_программирования/1.
:- discontiguous уровень_опыта/1.
:- discontiguous опыт_работы/1.
:- discontiguous формат_работы/1.
:- discontiguous зп/1.

% "Заглушки" для askable-предикатов, чтобы они существовали и не выдавали ошибку
язык_программирования(_) :- fail.
уровень_опыта(_) :- fail.
опыт_работы(_) :- fail.
формат_работы(_) :- fail.
зп(_) :- fail.

% Загрузка базы знаний кандидатов и базы опций из отдельных файлов
:- consult('candidates.pl').
:- consult('options_db.pl').

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% МЕХАНИЗМ ОБЪЯСНЕНИЯ И ДОКАЗАТЕЛЬСТВА
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
% МЕХАНИЗМ ЗАПРОСА С ОТЛОЖЕННЫМ СОХРАНЕНИЕМ ОТВЕТОВ
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
    ( A == почему ->
         ( Q = [Hypothesis <== Conditions | _] ->
               format("Выдвигается гипотеза: ~w\n", [Hypothesis]),
               format("при комплексе условий: ~w\n", [Conditions])
         ; true ),
         retractall(answer(Pred, _)),
         ask_attribute(G, NewAnswer),
         assertz(answer(Pred, NewAnswer)),
         ans_check(G, Q)
    ; A == как ->
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
% Предикаты для askable-атрибутов
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

askable(t(язык_программирования/_)).
askable(t(уровень_опыта/_)).
askable(t(опыт_работы/_)).
askable(t(формат_работы/_)).
askable(t(зп/_)).

askable(язык_программирования(_)).
askable(уровень_опыта(_)).
askable(опыт_работы(_)).
askable(формат_работы(_)).
askable(зп(_)).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Вспомогательные предикаты для меню
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
    append(OptionsNoWhy, [почему, как], Options),
    format("Выберите значение для ~w:\n", [Pred]),
    print_options(Options, 1),
    format("Ваш выбор (введите номер): "),
    read(Choice),
    ( integer(Choice),
      nth1(Choice, Options, Selected) ->
         Answer = Selected
    ; writeln('Неверный выбор, попробуйте снова.'),
      ask_attribute(G, Answer)
    ).

print_options([], _).
print_options([Opt|Rest], N) :-
    format("~w. ~w\n", [N, Opt]),
    N1 is N + 1,
    print_options(Rest, N1).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Сохранение информации о доказательствах и история
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

my_asserta(is_ans(G, V)) :-
    retract(is_ans(G, V)),
    assert(is_ans(G, V)), !.
my_asserta(is_ans(G, V)) :-
    assert(is_ans(G, V)), !.

% Определение списка атрибутов для истории
attributes([язык_программирования, уровень_опыта, опыт_работы, формат_работы, зп]).

% Модифицированный предикат story/0 для вывода истории в заданном формате
story :-
    writeln("История:"),
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
           ; true  % Пропускаем атрибуты, которые не были запрошены
           )
    ).

% Предикат для вывода укороченной истории на данный момент
short_story :-
    findall(P, (answer(P, A), A \== почему, A \== как), AskedAttrs),
    list_to_set(AskedAttrs, UniqueAttrs),
    ( UniqueAttrs = [] ->
        writeln("Нет запрошенных атрибутов на данный момент.")
    ;
        writeln("Укороченная история на данный момент:"),
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
% Вспомогательные предикаты для работы с кандидатами
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

conj([], true).
conj([G], G).
conj([G|Gs], (G, Rest)) :-
    conj(Gs, Rest).

wrap(P, Arg, Goal) :-
    Goal =.. [P, Arg].

read_languages(Languages) :-
    write('Введите язык программирования: '), read(Lang),
    read_languages_aux([Lang], Languages).

read_languages_aux(Acc, Languages) :-
    writeln('Добавить еще язык? (1 - Да, 2 - Перейти к следующему пункту)'),
    read(Choice),
    ( Choice = 1 ->
         write('Введите язык программирования: '), read(NextLang),
         append(Acc, [NextLang], NewAcc),
         read_languages_aux(NewAcc, Languages)
    ; Choice = 2 ->
         Languages = Acc
    ; writeln('Неверный выбор, считаем, что больше языков не добавляется.'),
         Languages = Acc
    ).

add_candidate :-
    write('Введите имя кандидата (например, ivan): '), read(Name),
    read_languages(Languages),
    forall(member(Lang, Languages), update_option_if_new(язык_программирования, Lang)),
    write('Введите уровень опыта (например, junior, middle, senior): '), read(Level),
    update_option_if_new(уровень_опыта, Level),
    write('Введите опыт работы (число лет, например, 5): '), read(WorkExp),
    update_option_if_new(опыт_работы, WorkExp),
    write('Введите формат работы (удаленка или очно): '), read(WorkFormat),
    update_option_if_new(формат_работы, WorkFormat),
    write('Введите зп (например, 30000 или 50000): '), read(Salary),
    update_option_if_new(зп, Salary),
    build_clause_body(Languages, Level, WorkExp, WorkFormat, Salary, Body),
    assertz((кандидат(Name) :- Body)),
    writeln('Новый кандидат добавлен в базу знаний.'),
    write_candidate_to_file(Name, Languages, Level, WorkExp, WorkFormat, Salary).

build_clause_body(Languages, Level, WorkExp, WorkFormat, Salary, Body) :-
    maplist(wrap(язык_программирования), Languages, LanguageGoals),
    conj(LanguageGoals, LanguagesConj),
    wrap(уровень_опыта, Level, LevelGoal),
    wrap(опыт_работы, WorkExp, WorkExpGoal),
    wrap(формат_работы, WorkFormat, FormatGoal),
    wrap(зп, Salary, SalaryGoal),
    Body = (LanguagesConj, LevelGoal, WorkExpGoal, FormatGoal, SalaryGoal).

write_candidate_to_file(Name, Languages, Level, WorkExp, WorkFormat, Salary) :-
    open('candidates.pl', append, Stream),
    format(Stream, '\n%% Новый кандидат\n', []),
    format(Stream, 'кандидат(~w) :-\n', [Name]),
    write_list_lines(Stream, Languages, 'язык_программирования'),
    format(Stream, '    ~w(~w),\n', ['уровень_опыта', Level]),
    format(Stream, '    ~w(~w),\n', ['опыт_работы', WorkExp]),
    format(Stream, '    ~w(~w),\n', ['формат_работы', WorkFormat]),
    format(Stream, '    ~w(~w).\n', ['зп', Salary]),
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

% Модифицированный run_expert с выбором после поиска
run_expert :-
    clear_history,
    ( prove(подбор(Кандидат), Proof, [])
      -> ( format("Результат подбора кандидата: ~w\n", [Кандидат]),
           writeln("Доказательство:"),
           writeln(Proof)
         )
      ; writeln('Не найден кандидат, удовлетворяющий условиям.')
    ),
    writeln('1. Показать историю'),
    writeln('2. Выход в меню'),
    read(Choice),
    ( Choice = 1 ->
         story
    ; Choice = 2 ->
         true
    ; writeln('Неверный выбор, возвращаемся в меню.')
    ).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Меню программы
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

menu :-
    writeln('Меню:'),
    writeln('1. Ввести нового кандидата'),
    writeln('2. Выполнить подбор кандидата'),
    writeln('3. Выход'),
    writeln('Выберите опцию (1, 2 или 3):'),
    read(Choice),
    ( Choice = 1 ->
         candidate_menu
    ; Choice = 2 ->
         run_expert,
         menu
    ; Choice = 3 ->
         writeln('Выход из программы.'),
         halt
    ; otherwise ->
         writeln('Неверный выбор, попробуйте снова.'),
         menu
    ).

candidate_menu :-
    add_candidate,
    writeln('Добавить еще кандидата? (1 - Да, 2 - Вернуться в главное меню)'),
    read(Choice),
    ( Choice = 1 ->
         candidate_menu
    ; Choice = 2 ->
         menu
    ; writeln('Неверный выбор, возвращаем в главное меню.'),
         menu
    ).

% Определение предиката подбора кандидата
подбор(Кандидат) :-
    кандидат(Кандидат).

:- initialization(menu).
