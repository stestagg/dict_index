import textwrap
from pathlib import Path
from datetime import datetime
import json

import click
import dateformat
from jinja2 import Environment, FileSystemLoader, select_autoescape, Markup
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter


JINJA_ENV = Environment(
    loader=FileSystemLoader([Path(__file__).parent]),
    autoescape=select_autoescape(['html', 'xml'])
)

HTML_FORMATTER = HtmlFormatter(style="monokai")
PROPOSAL_COLOR = '#2ca02c'
COLORS = ('#1f77b4', '#ff7f0e', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf')
PROPOSAL_NAMES = {'proposed', 'keys_index', 'items_index'}


def format_date(value, format='YYYY-MM-DD'):
    date = datetime.utcfromtimestamp(value)
    return dateformat.DateFormat(format).format(date)


def format_code(code):
    return Markup(highlight(code.rstrip(), PythonLexer(), HTML_FORMATTER))


JINJA_ENV.filters['date'] = format_date
JINJA_ENV.filters['code'] = format_code
JINJA_ENV.filters['num'] = lambda v: "{:,}".format(v)
JINJA_ENV.filters['dedent'] = textwrap.dedent


def load_results(path):
    all_results = []
    for child in path.iterdir():
        if child.suffix.lower() == ".json":
            result = json.loads(child.read_text())
            result['name'] = child.stem
            all_results.append(result)
    return all_results


def make_index(results, dest):
    content = JINJA_ENV.get_template('index.html').render(results=results)
    dest.write_text(content)


def reshape_results_for_chart(results):
    reshaped = []
    for cls_name, meth_results in results.items():
        cls_data = {
            'cls': cls_name,
            'series': []
        }
        reshaped.append(cls_data)

        for i, (meth_name, variants) in enumerate(meth_results.items()):
            color = COLORS[i]
            if meth_name in PROPOSAL_NAMES:
                meth_name = f'{meth_name}(*)'
                color = PROPOSAL_COLOR
            points = []
            point_data = {
                'name': f'{ meth_name }.runs',
                'color': color,
                'type': 'scatter',
                'showInLegend': False,
                'dataPoints': points
            }
            cls_data['series'].append(point_data)
            mins = []
            min_data = {
                'name': meth_name,
                'color': color,
                'type': 'spline',
                'showInLegend': True,
                'dataPoints': mins
            }
            cls_data['series'].append(min_data)
            
            for variant, times in variants.items():
                dict_size = int(variant)
                for time in times:
                    points.append({'x': dict_size, 'y': time})
                mins.append({'x': dict_size, 'y': min(times)})
            mins.sort(key=lambda x: x['x'])
    return reshaped

def reshape_results_for_table(results):
    reshaped = {}
    for cls_name, meth_raw in results.items():
        cls_results = {}
        cls_variants = set()
        reshaped[cls_name] = cls_results
        
        for meth_name, variants in meth_raw.items():
            cls_variants.update(variants.keys())

        cls_variants = sorted(int(v) for v in cls_variants)
        cls_results['variants'] = cls_variants
        meth_results = {}
        cls_results['meth'] = meth_results

        for meth_name, variants in meth_raw.items():
            meth_results[meth_name] = [None] * len(cls_variants)
            for i, variant in enumerate(cls_variants):
                times = variants.get(str(variant))
                if times is not None:
                    meth_results[meth_name][i] = min(times)
    return reshaped


def make_results_page(results, dest):
    style = HTML_FORMATTER.get_style_defs()
    chart_data = reshape_results_for_chart(results['results'])
    table_data = reshape_results_for_table(results['results'])
    content = JINJA_ENV.get_template('results.html').render(
        results=results, 
        style=style, 
        chart_data=chart_data,
        table_data=table_data,
        PROPOSAL_NAMES=PROPOSAL_NAMES,
    )
    dest.write_text(content)


@click.command()
@click.argument('result_dir')
@click.argument('output_dir')
def main(result_dir, output_dir):
    results_path = Path(result_dir)
    assert results_path.is_dir()

    output_dir = Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir()

    results = load_results(results_path)
    make_index(results, output_dir / 'index.html')
    for result in results:
        result_path = output_dir / f'{result["name"]}.html'
        make_results_page(result, result_path)


if __name__ == '__main__':
    main()