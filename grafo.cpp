#include <vcl.h>
#include <iostream>
#include <list>
#include <algorithm>
#include <conio>
#include <queue>
#include <stdio.h>
#include <fstream>
using namespace std;


typedef struct queue *QUEUE;
typedef struct node *link;
typedef struct gnode *bins;
typedef struct Glist *glist;
typedef struct graph *Graph;
typedef struct resp *Resp;
typedef struct req *Req;
typedef struct lreq *Lreq;
typedef struct ordem *Ordem;
typedef struct lord *Lord;
Graph GRAPHinit(int V);
void GRAPHinsertArc(Graph G,int V);
void desalocaMatriz(int ** r,int v);
int H,tamL=0;


/*estruturas*/
struct gnode{
        Graph g;
        bins next;
};

struct Glist{
        bins ini;
        bins fim;
        int q;
};

struct node{
        int w;
        link next;
};

/*struc de requisi�oes*/
struct ordem{
        int I;
        int O;
        int V;
        bool C;
        Ordem prox;
        };

struct lord{
        Ordem ini;
        };

struct graph{
        int V;
        int A;
        int IG;
        link *adj;
};

struct resp{
        int V;
        bool c;
        link next;
};

/*lista de resposta*/
struct req{
        int o;
        int f;
        Resp r;
        Req next;
};

struct lreq{
        Req ini;
        };

/*fun�oes para lista*/
int glist_vazia(glist l){
        if(l->ini == NULL ){
                if(l->fim == NULL)
                         return 1;
         }
        else
                return 0;}

glist crialista(){
        glist l = new struct Glist;
        l->ini =NULL;
        l-> fim =NULL;
        l->q=0;
        return l;
}



static link NEWnode( int w, link next){
        link a= new struct node ;
        a->w=w;
        a->next=next;
        return a;
}
/*fun�ao de criar um novo grafo*/
static glist NEWgnode(glist x,int v){
        bins novo = new struct gnode;
        novo->next = NULL;
        novo->g = GRAPHinit(v);
        if(glist_vazia(x)){
                x->ini = novo;
                x->fim = novo;
                x->q++;
                GRAPHinsertArc(novo->g,v);
                return x;
        }
        else
                x->fim->next = novo;
                x->fim = novo;
                x->q++;
                GRAPHinsertArc(novo->g,v);
                return x;



}


/*iniciar um grafo*/
Graph GRAPHinit(int V){
Graph G = new struct graph;
G->V=V;
G->A=0;
G->adj=new link[V];
for (int v=0; v<V; ++v){
        G->adj[v]=NULL;
        }
return G;}

 void GRAPHinsertArc(Graph G, int V){
 int i,j;
 link aux;
 int **ad= new int*[V];
 for(i=0;i<V;i++){
        ad[i] = new int[V];
}
 std::ifstream file ("adj.txt");
printf("\n");
if(!file){
        printf("\n Erro de leitura.");
        return ;
}
 for(i=0;i<V;i++){
   for(j=0;j<V;j++){
        file>>ad[i][j];
        printf(" %d ",ad[i][j]) ;
   }
      printf("\n");
}
 for(i=0;i<V;i++){
 for(j=0;j<V;j++){
        if(ad[i][j]==1){
                if(G->adj[i]==NULL){
                        G->adj[i]=NEWnode(j+1 ,G->adj[i]);
                                G->A++;}
                else{
                for(aux=G->adj[i];aux!=NULL;aux=aux->next){
                if(aux->w != j+1){
                        G->adj[i]=NEWnode(j+1 ,G->adj[i]);
                        G->A++;
                        break;}
                }}

        }

   }
 }

return;
}


 typedef struct link2 Link2;
struct link2
  {
    int dist;
    int visitado;
    int anterior;
  };

Resp dijkstra(int o, int f, Graph g)
  {
    Link2 *Q;
    int inf,menor, menor_id,tamQ;

    inf = g->V +1;
    Q = new Link2[g->V];
    tamQ = g->V;
    for (int i=0; i<g->V; i++)
      {
        /*Q[i]->id = i;*/
        if(i==o-1) Q[i].dist = 0;
        else Q[i].dist = inf;
        Q[i].visitado = 0;
        Q[i].anterior = -1;

      }
    menor_id = o;
    menor = 0;
    while((tamQ>0)&&(menor<inf))
      {
        for(link j = g->adj[menor_id-1]; j !=NULL; j = j->next)
          {
            if(!Q[j->w-1].visitado)
              {
                int dist_aux = Q[menor_id-1].dist + 1;
                if (dist_aux<Q[j->w-1].dist)
                  {
                    Q[j->w-1].dist = dist_aux;
                    Q[j->w-1].anterior = menor_id;
                  }
              }
          }
        Q[menor_id-1].visitado =1;
        if (menor_id == f) break;
        tamQ = tamQ-1;
        menor= g->V +1;
        if (tamQ >0)
          {
            for(int i = 0; i < g->V; i++)
              {
                if (!Q[i].visitado)
                  {
                    if (Q[i].dist < menor)
                      {
                        menor_id = i+1;
                        menor = Q[i].dist;
                      }
                  }
              }
          }
      }
      Resp r = new struct resp;
      if (Q[f-1].visitado)
        {
          r->V = Q[f-1].dist;
          r->c =1;
          r->next = NULL;

          int id = f;
          r->next = NEWnode(id,r->next);
          while(id !=o)
            {
              id = Q[id-1].anterior;
              r->next = NEWnode(id,r->next);
            }
        }
      else
        {
          r->V = g->V+1;
          r->c = 0;
          r->next = NULL;
        }
      return r;
    }

/*fun�ao para excluir o caminho ja usado*/
void exclui_aresta(Graph g , Resp r){
printf("\n exclui aresta");
        link i,j,k;
        int m;
        for(i=r->next, j= r->next->next; j!=NULL;i=j,j=j->next){
                m=i->w;
                for(k=g->adj[m-1]; k!=NULL; k=k->next){
                        if(k->w== j->w){
                                link aux = k;
                                g->adj[m-1]= k ->next;
                                free (aux);
                                break;
                                }
                }
        }

}
/*criando estrutura de requisi�oes*/
Lord requisicoes(int V){
glist O;
O=crialista();
O=NEWgnode(O,V);
link q;
int i,j;
Lord Vord = new struct lord;
Vord->ini=NULL;
Ordem l;
int **or=new int*[V];

for(i=0;i<V;i++){
        or[i] = new int[V];
        }

int **r=new int*[V];
for(i=0;i<V;i++){
        r[i] = new int[V];
        }


/*ordena�ao das requisi�oes*/
std::ifstream file1 ("ord.txt");

if(!file1){
        cout<<"\n Erro de leitura.";
        }

for(i=0;i<V;i++){
   for(j=0;j<V;j++){
        file1>>or[i][j];
   }
      printf("\n");
}

/*fechar arquivo*/
file1.close();

std::ifstream file ("matriz.txt");

if(!file){
        printf("\n Erro de leitura.");
        return 0;
}
for(i=0;i<V;i++){
   for(j=0;j<V;j++){
        file>>r[i][j];
   }
}
file.close();

for(i=0;i<V;i++){
        for(j=0;j<V;j++){
                while(or[i][j]!=0){
                Resp ord = new struct resp;
                ord = NULL;
                ord=dijkstra(i+1,j+1,O->ini->g);
                if(ord->c==1){
                        or[i][j]--;
                        while(r[i][j]!=0){
                                Ordem OR= new struct ordem;
                                OR->I=i+1;
                                OR->O=j+1;
                                OR->V=ord->V;
                                OR->C=1;
                                OR->prox=Vord->ini;
                                Vord->ini = OR;
                                r[i][j]--;
                                tamL++;
                                }
                        }
                }

        }
}
 desalocaMatriz(or,V);
 desalocaMatriz(r,V);

return Vord;
}

/*desaloca link*/
void desalocalink(link a){
link aux = a;
link del;
while(aux != NULL ){
        del = aux;
        aux = aux->next;
        delete del ;
}
delete aux;
}

/*Desalocar grafo*/

desalocaGrafo(Graph g, int v){

link aux;
int i ;
for (i=0;i<v;i++){
        desalocalink(g->adj[i]);

}
delete g->adj;

delete g;

}

/*Desalocar lista de grafo*/

desalocaglist(glist B){
bins aux,del;
aux = B->ini;

while(aux != NULL ){
        del = aux;
        aux = aux->next;
        desalocaGrafo(del->g,del->g->V);
}
delete aux;
delete B->ini;
delete B->fim;
delete B;
}


/* Desalocar a Lord*/
void desalocaLord(Lord l){
Ordem aux=l->ini;
Ordem del;

while(aux != NULL ){
        del = aux;
        aux = aux->prox;
        delete del ;
}

delete l;
}

/*Randomizar a lista de requisi�oes*/
Lord randomiza (Lord l){
int * rd = new int[tamL];
int i,x,aux;
printf("\nVetor sem ordenar\n\n");
for(i=0;i<tamL;i++){
        rd[i] = i+1; /* inicializa o vetor com as posic�es da lista*/
}
for(i=0;i<tamL ;i++){
        x = (rand()%(tamL-1)); //gera numero aleatorio de 1 ate tamL
        aux = rd[i];
        rd[i]= rd[x];
        rd[x] = aux;
}

Lord Vord = new struct lord;
Vord->ini=NULL;
Ordem j; int cnt;
for(i=0;i<tamL;i++){
        x= rd[i]; /*vai inserir a posi��o X da lista na nova lista*/

        for(j=l->ini,cnt=1;j!=NULL;j=j->prox,cnt++) {
                if(cnt == x){     /*percorre a lista ate a posi��o desejada*/
                        Ordem OR= new struct ordem;  /* vai copiar as informa�oes para um novo struct Ordem*/
                        OR->I=j->I;
                        OR->O=j->O;
                        OR->V=j->V;
                        OR->C=1;
                        OR->prox=Vord->ini;
                        Vord->ini = OR;
                        break;
                }
        }
}

desalocaLord(l); /*desaloca a lista q estava sequencial*/
delete []rd;
return Vord;   /*retorna a nova lista randomizada*/

}


/*Ordenando q lista de requisi�oes*/
Lord ordena(Lord l){
int r,t,y;
Ordem k,i;
for(i=l->ini;i!=NULL;i=i->prox){
        for(Ordem j= i->prox;j!=NULL;j=j->prox){

                if(i->V < j->V){

                        r=i->I;
                        t=i->O;
                        y=i->V;
                        i->I=j->I;
                        i->O=j->O;
                        i->V=j->V;
                        j->I = r;
                        j->O = t;
                        j->V = y;
                        }
                }

}
H=l->ini->V;
cout<<"\nH: "<<H;

return l;
}

/*desaloca matriz*/

void desalocaMatriz(int ** r,int v){
int i;

for(i=0;i<v;i++){
        delete r[i];

}
delete []r;
}


void kapov(Lord k,glist A,int v){
bins aux;
int i,j;
link te;
Ordem l;
int soma=0;
for(l=k->ini;l!=NULL;l=l->prox){
        i=l->I;
        j=l->O;
        Resp road = new struct resp;
        road = NULL;
        aux=A->ini;
        while(l->C){
                road=dijkstra(i,j,aux->g);
                printf("\n tem caminho de %d para %d: %d",l->I,l->O, road->c);
                for(te=road->next;te!=NULL;te=te->next){
                printf("\nC:%d",te->w);}
                cout<<"\nTamanho: "<<road->V;
                if(road->c==1 && road->V <= H){
                        exclui_aresta(aux->g, road);
                        l->C=0;
                        soma=soma+road->V;
                        }

                else if(road->V > H && aux->next!=NULL){
                        cout<<"\nENTREI E FUI PARA O PROXIMO GRAFO";
                        aux=aux->next;
                        }

                else if(road->V > H && aux->next==NULL){
                        A=NEWgnode(A,v);
                        GRAPHinsertArc(A->ini->g,v);
                        aux=A->fim;
                        }

                printf("\nG:%d",A->q);
                }
}

cout<<"\nSomatorio:"<<soma;
cout<<"\nTamanho:"<<tamL;

}






void gulosa(Lord k,glist C,int V){
bins aux;
int i,j;
link te;
Ordem l;
int soma=0;

for(l=k->ini;l!=NULL;l=l->prox){
        i=l->I;
        j=l->O;
        Resp road = new struct resp;
        road = NULL;
        aux=C->ini;
        while(l->C){
                road=dijkstra(i,j,aux->g);
                printf("\n tem caminho de %d para %d: %d",l->I,l->O, road->c);
                for(te=road->next;te!=NULL;te=te->next){
                printf("\nC:%d",te->w);}
                cout<<"\nTamanho: "<<road->V;
                if(road->c==1){
                        exclui_aresta(aux->g, road);
                        l->C=0;
                        soma=soma+road->V;
                        }
                else if(road->c==0 && aux->next!=NULL){
                        aux=aux->next;
                        }
                else if(road->c==0 && aux->next == NULL){
                        C=NEWgnode(C,V);
                        GRAPHinsertArc(C->ini->g,V);
                        aux=C->fim;
                        }
                printf("\nG:%d",C->q);
                }
}
cout<<"\nSomatorio:"<<soma;
cout<<"\nTamanho:"<<tamL;

}



int main(){
glist B;
int v,y,i,j;
link te;

/*leitura do arquivo com o numero de nos*/
std::ifstream file2 ("tamanho.txt");

if(!file2){
        printf("\n Erro de leitura.");
        return 0;}
file2>>v;

file2.close();
int **r =new int*[v];
for(i=0;i<v;i++){
        r[i] = new int[v];
        }

/*leitura do arquivo com as requisi�oes*/
std::ifstream file ("matriz.txt");

if(!file){
        printf("\n Erro de leitura.");
        return 0;
}
for(i=0;i<v;i++){
   for(j=0;j<v;j++){
        file>>r[i][j];
   }
}
file.close();

B=crialista();
B=NEWgnode(B,v);

Lord Lordena= requisicoes(v);
Ordem l,k;
Lordena = randomiza(Lordena);
Lordena = ordena(Lordena);

/*mostrando a lista de requisi�oes ordenada*/
for(k=Lordena->ini; k!=NULL; k=k->prox){
        cout << "\n\n\nOrigem: "<< k->I;
        cout << "\nDestino: " << k->O;
        cout << "\nTamanho: " << k->V;
        }

kapov(Lordena, B,v);
/*gulosa(Lordena,B,v);*/


        printf("\n");
for(i=0;i<v;i++){
        for(j=0;j<v;j++){
                printf(" %d ",r[i][j]);}
                printf("\n");
                }




desalocaglist(B);
desalocaLord (Lordena);
desalocaMatriz(r,v);

getch();

        return 0;
}

