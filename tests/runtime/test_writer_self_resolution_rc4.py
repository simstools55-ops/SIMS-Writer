from runtime.sims_writer_runtime.editorial_decision import classify_change, build_publication_result, PUBLIC_OK, USER_DECISION, INTERNAL_REJECT


def test_generic_editorial_choice_is_not_delegated_to_user():
    change={
        "component":"article_title", "before":"妊娠中でも働けるコールセンター｜体験談・注意点",
        "after":"妊娠中でも働けるコールセンター｜伝えるタイミング・注意点",
        "requires_user_confirmation":True,
        "evidence_level":"MEDIUM",
        "reason":"本文に体験談が存在せず、既存本文の主題に合わせて約束を修正",
    }
    assert classify_change(change)==PUBLIC_OK


def test_owner_only_experience_fact_remains_user_decision():
    change={
        "component":"body", "before":"", "after":"私は妊娠中にコールセンターで働きました。",
        "decision_signals":["author_experience"],
        "user_confirmation_kind":"experience",
        "evidence_level":"MEDIUM",
    }
    assert classify_change(change)==USER_DECISION
    result=build_publication_result([change])
    item=result["user_decision_changes"][0]
    assert item["blocking"] is True
    assert item["response_options"]==["YES","NO"]
    assert item["question"]


def test_low_evidence_is_internal_reject_not_user_homework():
    change={"component":"faq","before":"なし","after":"未確認の新事実","evidence_level":"LOW"}
    assert classify_change(change)==INTERNAL_REJECT


def test_presentation_renders_explicit_user_question_and_blocks_registration():
    from runtime.sims_writer_runtime.presentation_formatter import build_human_presentation, render_human_markdown
    publication={
        "public_ok_changes":[],
        "user_decision_changes":[{
            "component":"body", "component_label":"実体験",
            "decision_reason":"本人だけが実体験の有無を確定できるため",
            "question":"妊娠中に実際にコールセンターで働いた経験がありますか？",
            "response_options":["YES","NO"], "blocking":True,
        }],
    }
    presentation=build_human_presentation(publication)
    md=render_human_markdown(presentation)
    assert "## 利用者判断" in md
    assert "YES / NO" in md
    assert "再生成してからSBMへ登録" in md
