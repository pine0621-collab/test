"""
프롬프트 템플릿 로더
YAML 기반 템플릿 로드 및 관리
"""

import os
from pathlib import Path
from typing import Dict, Any, List, Optional
import yaml
from dataclasses import dataclass


@dataclass
class PromptTemplate:
    """프롬프트 템플릿 데이터 클래스"""
    id: str
    name: str
    description: str
    system_prompt: str
    user_prompt_template: str
    output_format: Any
    parameters: Dict[str, Any]

    def render_user_prompt(self, **kwargs) -> str:
        """
        사용자 프롬프트 렌더링

        Args:
            **kwargs: 템플릿 변수

        Returns:
            렌더링된 프롬프트
        """
        prompt = self.user_prompt_template
        for key, value in kwargs.items():
            placeholder = "{" + key + "}"
            if placeholder in prompt:
                prompt = prompt.replace(placeholder, str(value))
        return prompt


class TemplateLoader:
    """프롬프트 템플릿 로더"""

    def __init__(self, templates_path: str = None):
        """
        Args:
            templates_path: 템플릿 디렉토리 경로
        """
        if templates_path is None:
            self.base_path = Path(__file__).parent.parent / "prompts"
        else:
            self.base_path = Path(templates_path)

        self.templates: Dict[str, PromptTemplate] = {}
        self._load_templates()

    def _load_templates(self):
        """모든 템플릿 로드"""
        if not self.base_path.exists():
            return

        for yaml_file in self.base_path.glob("*.yaml"):
            template = self._load_template_file(yaml_file)
            if template:
                self.templates[template.id] = template

    def _load_template_file(self, file_path: Path) -> Optional[PromptTemplate]:
        """단일 템플릿 파일 로드"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            return PromptTemplate(
                id=data.get("id", file_path.stem),
                name=data.get("name", ""),
                description=data.get("description", ""),
                system_prompt=data.get("system_prompt", ""),
                user_prompt_template=data.get("user_prompt_template", ""),
                output_format=data.get("output_format", {}),
                parameters=data.get("parameters", {})
            )
        except Exception as e:
            print(f"템플릿 로드 실패 ({file_path}): {e}")
            return None

    def get_template(self, template_id: str) -> Optional[PromptTemplate]:
        """템플릿 조회"""
        return self.templates.get(template_id)

    def list_templates(self) -> List[Dict[str, str]]:
        """사용 가능한 템플릿 목록"""
        return [
            {
                "id": t.id,
                "name": t.name,
                "description": t.description
            }
            for t in self.templates.values()
        ]

    def get_template_parameters(self, template_id: str) -> Dict[str, Any]:
        """템플릿 파라미터 정보 조회"""
        template = self.get_template(template_id)
        if template:
            return template.parameters
        return {}

    def validate_parameters(self, template_id: str, params: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        파라미터 유효성 검사

        Returns:
            {"errors": [...], "warnings": [...]}
        """
        result = {"errors": [], "warnings": []}

        template = self.get_template(template_id)
        if not template:
            result["errors"].append(f"템플릿을 찾을 수 없습니다: {template_id}")
            return result

        for param_name, param_config in template.parameters.items():
            # 필수 파라미터 체크
            if param_config.get("required", False) and param_name not in params:
                result["errors"].append(f"필수 파라미터 누락: {param_name}")

            # 옵션 값 체크
            if param_name in params and "options" in param_config:
                if params[param_name] not in param_config["options"]:
                    result["warnings"].append(
                        f"'{param_name}'의 값 '{params[param_name]}'이 "
                        f"권장 옵션에 없습니다: {param_config['options']}"
                    )

        return result


# 사용 예시
if __name__ == "__main__":
    loader = TemplateLoader()

    print("=== 사용 가능한 템플릿 ===")
    for t in loader.list_templates():
        print(f"- {t['id']}: {t['name']} - {t['description']}")

    print("\n=== blog_post 템플릿 파라미터 ===")
    params = loader.get_template_parameters("blog_post")
    for name, config in params.items():
        print(f"- {name}: {config.get('description', '')} "
              f"(필수: {config.get('required', False)})")
