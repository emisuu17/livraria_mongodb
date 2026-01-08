from flask import render_template, request, redirect, url_for
from app import app
from models import buscar_livros, buscar_livro_por_id, obter_categorias

@app.route('/')
def index():
    # Pega os parâmetros da URL
    termo = request.args.get('busca', '')
    pagina = int(request.args.get('page', 1))
    
    # chama a função do models.py
    livros, total_livros = buscar_livros(termo=termo, pagina=pagina)
    
    # aqui faz o calculo se tem próxima pagina
    tem_proxima = (total_livros > (pagina * 10))
    
    return render_template(
        'index.html', 
        livros=livros, 
        termo_busca=termo,
        pagina_atual=pagina,
        tem_proxima=tem_proxima
    )

@app.route('/livro/<id_livro>')
def detalhe_livro(id_livro):
    # Busca o livro específico
    livro = buscar_livro_por_id(id_livro)
    
    if not livro:
        return redirect(url_for('index'))
        
    return render_template('detalhe.html', livro=livro)

